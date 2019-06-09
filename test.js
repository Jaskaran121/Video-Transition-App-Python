//https://dev.to/phil/the-best-way-to-test-redux-sagas-4hib
import billing from './billing'
import billingService from 'services/billing'
import {queryBilling, updatePrimaryBillingContact} from 'services/billing'
import {call, put, select} from 'redux-saga/effects';
describe('billing', ()=>{
    describe('namespace',()=>{
        it('Should have correct name', () => {
          
            // spyOn(billingService, 'queryBilling').and.callFake(()=> {
            //     return Promise.resolve()
            // })
            // expect(billing.namespace).toEqual('billing')
            
            //Just checks if it is a call to queryBilling without actually calling the queryBilling
            const action = () => { }
            const gen = billing.effects.query(action,{call,put})
            const returnedValue = {"done": false,"value":call(queryBilling)}
            expect(gen.next()).toEqual(returnedValue)
        })
    })
})
