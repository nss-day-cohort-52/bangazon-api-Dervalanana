from ast import Or
from bangazon_api.models.payment_type import PaymentType
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models import Order, Product


class OrderTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=2)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)

        self.user2 = User.objects.filter(store=None).last()
        product = Product.objects.get(pk=1)

        self.order1 = Order.objects.create(
            user=self.user1
        )

        self.order1.products.add(product)


        self.order2 = Order.objects.create(
            user=self.user2
        )


        self.order2.products.add(product)
        
        self.payment1= PaymentType.objects.create(
            customer=self.user1
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_complete_order(self):
        """A order which has a payment method assigned should be closed"""
        data = {
            "paymentTypeId": self.payment1.id
        }
        response = self.client.put(f'/api/orders/{self.order1.id}/complete', data, format='json')
        print(response.data)
        checkedorder = Order.objects.get(pk=self.order1.id)
        self.assertIsNotNone(checkedorder.completed_on)

    def test_delete_order(self):   
        response = self.client.delete(f'/api/orders/{self.order1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_orders(self):
        """The orders list should return a list of orders for the logged in user"""
        response = self.client.get('/api/orders')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    # TODO: Complete Order test
        
