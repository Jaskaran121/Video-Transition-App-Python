# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 23:35:38 2019

@author: Jaskaran Kukreja
"""

import sys

import cv2  # Install OpenCV
import numpy as np  # Install NumPy
from PIL import Image  # Install PILLOW (PIL)
from PyQt5.QtCore import QTimer  # Install PyQt5
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class mainwindow(QMainWindow):
    vid1 = []
    vid2 = []
    vid3 = []
    x0 = 0
    x1 = 0
    x2 = 0
    l2 = 0

    def __init__(self):
        super(mainwindow, self).__init__()
        loadUi('main.ui', self)  # Load the GUI

        self.cap = cv2.VideoCapture('1.mp4')
        self.cap1 = cv2.VideoCapture('2.mp4')
        self.capture2 = cv2.VideoCapture('3.avi')
        self.success, self.i0 = self.cap.read()
        self.a, self.i1 = self.cap1.read()
        self.ret, self.image2 = self.capture2.read()
        print(self.ret)

        while self.success:
            self.success, self.i0 = self.cap.read()
            self.vid1.append(self.i0)
        while self.a:
            self.a, self.i1 = self.cap1.read()
            self.vid2.append(self.i1)
        while self.ret:
            self.ret, self.image2 = self.capture2.read()
            self.vid3.append(self.image2)

        self.l2 = len(self.vid3)
        self.l0 = len(self.vid1)
        self.l1 = len(self.vid2)
        # Read your files here...

        self.display(self.vid1[0], 1)
        self.display1(self.vid2[0], 1)
        self.display2(self.vid1[0], 1)
        self.stop1 = True
        self.stop2 = True
        self.stopc = True
        self.play1.clicked.connect(self.getVideo1)
        self.pause1.clicked.connect(self.pauseVideo1)
        self.play2.clicked.connect(self.getVideo2)
        self.pause2.clicked.connect(self.pauseVideo2)
        self.playc.clicked.connect(self.getVideo3)
        self.pausec.clicked.connect(self.pauseVideoC)
        self.convert.clicked.connect(self.convert1)
        self.fade.setChecked(True)



    def convert1(self):
        if(self.fade.isChecked()):
            self.fade_convert()

        if(self.cut.isChecked()):
            self.cut_convert()

        if(self.wipe.isChecked()):
            self.wipe_convert()

        if (self.scale.isChecked()):
            self.scale_convert()

        if (self.picInPic.isChecked()):
            self.picInPic_convert()

        self.vid3 = []
        self.stopc = False
        self.capture2 = cv2.VideoCapture('3.avi')
        self.ret, self.image2 = self.capture2.read()
        while self.ret:
            self.ret, self.image2 = self.capture2.read()
            self.vid3.append(self.image2)

        self.stopc = True
        self.l2 = len(self.vid3)
        self.display(self.vid3[0], 1)


    def cut_convert(self):
        out = cv2.VideoWriter('3.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (640, 480))

        for i in np.concatenate((self.vid1, self.vid2)):
            out.write(i)
            cv2.waitKey(1)

        out.release()


    def fade_convert(self):
        out = cv2.VideoWriter('3.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (640, 480))
        length = len(self.vid1)
        length1 = len(self.vid2)
        count = 1
        for i in range(0, length):
            if (i > length - 30):

                img_CVFormat_Left = cv2.cvtColor(self.vid1[i-1], cv2.COLOR_BGR2RGB)
                img_PILFormat_Left = Image.fromarray(img_CVFormat_Left)

                img_CVFormat_Right = cv2.cvtColor(self.vid2[count - 1], cv2.COLOR_BGR2RGB)
                img_PILFormat_Right = Image.fromarray(img_CVFormat_Right)

                new_Image = Image.blend(img_PILFormat_Left, img_PILFormat_Right, 0.034 * count)

                final_CVFormat = cv2.cvtColor(np.array(new_Image), cv2.COLOR_RGB2BGR)
                out.write(final_CVFormat)
                count += 1
                if (i == length - 1):
                    for j in range(30, length1):
                        out.write(self.vid2[j])
                        cv2.waitKey(1)
                cv2.waitKey(1)

            else:
                out.write(self.vid1[i])
                cv2.waitKey(1)
        out.release()


    def wipe_convert(self):
        out = cv2.VideoWriter('3.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (640, 480))

        length = len(self.vid1)
        length1 = len(self.vid2)
        count = 1
        for i in range(0, length):
            if (i > length - 30):

                img_CVFormat_Left = cv2.cvtColor(self.vid1[i - 1], cv2.COLOR_BGR2RGB)
                img_PILFormat_Left = Image.fromarray(img_CVFormat_Left)

                img_CVFormat_Right = cv2.cvtColor(self.vid2[count - 1], cv2.COLOR_BGR2RGB)
                img_PILFormat_Right = Image.fromarray(img_CVFormat_Right)

                img_Left = img_PILFormat_Left.crop((0, 480* count / 30, 640, 480))
                img_Right = img_PILFormat_Right.crop((640, 0, 640 , 480 * count / 30))

                new_Image = Image.new("RGB", (640, 480))

                new_Image.paste(img_Left, (0, 0))
                new_Image.paste(img_Right, (img_Left.size[0], 0))

                final_CVFormat = cv2.cvtColor(np.array(new_Image), cv2.COLOR_RGB2BGR)
                out.write(final_CVFormat)

                count += 1
                if (i == length - 1):
                    for j in range(30, length1):
                        out.write(self.vid2[j])
                        cv2.waitKey(1)
                cv2.waitKey(1)

            else:
                out.write(self.vid1[i])
                cv2.waitKey(1)

        out.release()


    def scale_convert(self):
        out = cv2.VideoWriter('3.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (640, 480))
        length = len(self.vid1)
        length1 = len(self.vid2)
        count = 15
        for i in range(0, length):
            if (i > length - 15):
                if (count > 0):
                    img_CVFormat_Left = cv2.cvtColor(self.vid1[i - 1], cv2.COLOR_BGR2RGB)
                    img_PILFormat_Left = Image.fromarray(img_CVFormat_Left)
                    if (i == length - 1):
                        offset1 = (int(64), int(48))
                    else:
                        offset1 = (int(640 * 0.0667 * count), int(480 * 0.0667 * count))
                    vid1_scaled = img_PILFormat_Left.resize(offset1, Image.BICUBIC)

                    # creating background
                    background = Image.new('RGBA', (640, 480), (0, 0, 0, 0))
                    bg_w, bg_h = background.size
                    img_w, img_h = vid1_scaled.size
                    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
                    background.paste(vid1_scaled, offset)
                    final_CVFormat_vid1 = cv2.cvtColor(np.array(background), cv2.COLOR_RGB2BGR)
                    out.write(final_CVFormat_vid1)
                    cv2.waitKey(1)

                    count -= 1

                if (i == length - 1):
                    count1 = 1
                    for j in range(0, length1):
                        if (j < 15):
                            img_CVFormat_Right = cv2.cvtColor(self.vid2[j], cv2.COLOR_BGR2RGB)
                            img_PILFormat_Right = Image.fromarray(img_CVFormat_Right)
                            if (j == 0):

                                offset = (int(64), int(48))
                            else:
                                offset = (int(640 * 0.0667 * count1), int(480 * 0.0667 * count1))
                            vid2_scaled = img_PILFormat_Right.resize(offset, Image.BICUBIC)

                            # creating background

                            background_vid2 = Image.new('RGBA', (640, 480), (0, 0, 0, 0))
                            bg_w2, bg_h2 = background_vid2.size
                            img_w2, img_h2 = vid2_scaled.size
                            offset = ((bg_w2 - img_w2) // 2, (bg_h2 - img_h2) // 2)
                            background_vid2.paste(vid2_scaled, offset)
                            final_CVFormat_vid2 = cv2.cvtColor(np.array(background_vid2), cv2.COLOR_RGB2BGR)
                            out.write(final_CVFormat_vid2)
                            count1 += 1
                        else:
                            out.write(self.vid2[j])
                            cv2.waitKey(1)

            else:
                out.write(self.vid1[i])
                cv2.waitKey(1)

        out.release()


    def picInPic_convert(self):
        out = cv2.VideoWriter('3.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (640, 480))

        length = len(self.vid1)
        length1 = len(self.vid2)
        count = 1
        for i in range(0, length):

            if (i > length - 30):

                img_CVFormat_Vid1 = cv2.cvtColor(self.vid1[i - 1], cv2.COLOR_BGR2RGB)
                img_PILFormat_Vid1 = Image.fromarray(img_CVFormat_Vid1)

                img_CVFormat_Vid2 = cv2.cvtColor(self.vid2[count - 1], cv2.COLOR_BGR2RGB)
                img_PILFormat_Vid2 = Image.fromarray(img_CVFormat_Vid2)

                vid1_w, vid1_h = img_PILFormat_Vid1.size
                img_PILFormat_Vid3 = img_PILFormat_Vid2.resize((int(vid1_w * 0.034 * count),
                                                                int(vid1_h * 0.034 * count)))
                vid3_w, vid3_h = img_PILFormat_Vid3.size

                img_PILFormat_Vid1.paste(img_PILFormat_Vid3, (vid1_w - vid3_w, 0))

                final_CVFormat = cv2.cvtColor(np.array(img_PILFormat_Vid1), cv2.COLOR_RGB2BGR)
                out.write(final_CVFormat)

                count += 1
                if (i == length - 1):
                    for j in range(30, length1):
                        out.write(self.vid2[j])
                        cv2.waitKey(1)
                cv2.waitKey(1)

            else:
                out.write(self.vid1[i])
                cv2.waitKey(1)

        out.release()






    def getVideo1(self):  # Playing Video 1
        if self.stop1:
            self.timer0 = QTimer(self)
            self.timer0.timeout.connect(self.update_frame)
            self.timer0.start(33.34)
            self.stop1 = False

    def getVideo2(self):  # Playing Video 2
        if self.stop2:
            self.timer1 = QTimer(self)
            self.timer1.timeout.connect(self.update_frame1)
            self.timer1.start(33.34)
            self.stop2 = False

    def getVideo3(self):  # Playing Converted Video
        if self.stopc:
            self.timer2 = QTimer(self)
            self.timer2.timeout.connect(self.update_frame2)
            self.timer2.start(33.34)
            self.stopc = False

    def pauseVideo1(self):
        self.timer0.stop()
        self.stop1 = True

    def pauseVideo2(self):
        self.timer1.stop()
        self.stop2 = True

    def pauseVideoC(self):
        self.timer2.stop()
        self.stopc = True

    def update_frame(self):
        if self.x0 < self.l0:
            self.display(self.vid1[self.x0], 1)
            self.x0 += 1
        else:
            self.x0 = 0

    def update_frame1(self):
        if self.x1 < self.l1:
            self.display1(self.vid2[self.x1], 1)
            self.x1 += 1
        else:
            self.x1 = 0

    def update_frame2(self):
        if self.x2 < self.l2:
            self.display2(self.vid3[self.x2], 1)
            self.x2 += 1
        else:
            self.x2 = 0

    def display(self, img, window=1):
        qformat = QImage.Format_Indexed8
        qformat = QImage.Format_RGB888
        outImage = QImage(img, 640, 480, qformat)
        outImage = outImage.rgbSwapped()
        if window == 1:
            self.video1.setPixmap(QPixmap.fromImage(outImage))
            self.video1.setScaledContents(True)

    def display1(self, img, window=1):
        qformat = QImage.Format_Indexed8
        qformat = QImage.Format_RGB888
        outImage = QImage(img, 640, 480, qformat)
        outImage = outImage.rgbSwapped()
        if window == 1:
            self.video2.setPixmap(QPixmap.fromImage(outImage))
            self.video2.setScaledContents(True)

    def display2(self, img, window=1):
        qformat = QImage.Format_Indexed8
        qformat = QImage.Format_RGB888
        outImage = QImage(img, 640, 480, qformat)
        outImage = outImage.rgbSwapped()
        if window == 1:
            self.convertedVideo.setPixmap(QPixmap.fromImage(outImage))
            self.convertedVideo.setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainwindow()
    window.setWindowTitle('Assignment1 SOEN6761')
    window.show()
    sys.exit(app.exec_())
