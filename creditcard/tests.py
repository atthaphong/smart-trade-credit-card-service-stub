"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from creditcard.models import  Account
from creditcard import views

class AccountTest(TestCase):
    def setUp(self):
        self.before_balance = 10000
        self.account = Account.objects.create(number='1234567812345678',ccv='000',balance=self.before_balance)

    def tearDown(self):
        self.account.delete()

    def test_successfully_verify(self):
        amount = 1000
        card_num = '1234567812345678'
        card_ccv = '000'
        params = {
            'card_num' : card_num,
            'card_ccv' : card_ccv,
            'amount' : amount
        }


        url = '/verify'
        response = self.client.post(url,params)
        print(response)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.content,views.SUCCESS)
        self.assertEqual(Account.objects.get(number=card_num,ccv=card_ccv).balance,self.before_balance)

    def test_failed_verify_wrong_amount(self):
        amount = 100000000
        card_num = '1234567812345678'
        card_ccv = '000'
        params = {
            'card_num' : card_num,
            'card_ccv' : card_ccv,
            'amount' : amount
        }
        url = '/verify'
        response = self.client.post(url,params)
        print(response)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.content,views.FAILED)
        self.assertEqual(Account.objects.get(number=card_num,ccv=card_ccv).balance,self.before_balance)


    def test_failed_verify_wrong_card(self):
        amount = 1000
        card_num = '1234567812345670'
        card_ccv = '000'
        params = {
            'card_num' : card_num,
            'card_ccv' : card_ccv,
            'amount' : amount
        }

        url = '/verify'
        response = self.client.post(url,params)
        print(response)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.content,views.FAILED)


    def test_failed_verify_wrong_ccv(self):
            params = {
                'card_num' : '1234567812345678',
                'card_ccv' : '001',
                'amount' : '1000'
            }

            url = '/verify'
            response = self.client.post(url,params)
            print(response)

            self.assertEqual(response.status_code,200)
            self.assertEqual(response.content,views.FAILED)

    def test_failed_pay_wrong_amount(self):
        params = {
            'card_num' : '1234567812345678',
            'card_ccv' : '000',
            'amount' : '99999999'
        }

        url = '/pay'
        response = self.client.post(url,params)
        print(response)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.content,views.FAILED)
        self.assertEqual(self.account.balance,self.before_balance)


    def test_failed_pay_wrong_card(self):
        amount = 1000
        card_num = '1234567812345671'
        card_ccv = '000'
        params = {
            'card_num' : card_num,
            'card_ccv' : card_ccv,
            'amount' : amount
        }

        url = '/pay'
        response = self.client.post(url,params)
        print(response)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.content,views.FAILED)

    def test_successfully_paid(self):
        amount = 1000
        card_num = '1234567812345678'
        card_ccv = '000'
        params = {
            'card_num' : card_num,
            'card_ccv' : card_ccv,
            'amount' : amount
        }

        url = '/pay'
        response = self.client.post(url,params)
        print(response)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.content,views.SUCCESS)
        self.assertEqual(Account.objects.get(number=card_num,ccv=card_ccv).balance,self.before_balance-amount)

