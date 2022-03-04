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
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)

        self.user2 = User.objects.filter(store=None).last()
        product = Product.objects.get(pk=1)

        # self.order1 = Order.objects.create(
        #     user=self.user1
        # )

        # self.order1.products.add(product)


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
        moddedOrder = self.client.get('/api/orders/current')
        response = self.client.put(f'/api/orders/{moddedOrder.data["id"]}/complete', data, format='json')
        print(response.data)
        checkedorder = Order.objects.get(pk=moddedOrder.data["id"])
        self.assertIsNotNone(checkedorder.completed_on)

    def test_delete_order(self):   
        moddedOrder = self.client.get('/api/orders/current')
        response = self.client.delete(f'/api/orders/{moddedOrder.data["id"]}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_orders(self):
        """The orders list should return a list of orders for the logged in user"""
        response = self.client.get('/api/orders')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) #should have 1 open, 1 closed
    
    def test_add_product(self):
        """ensure that newly added products get added to incomplete orders only"""
        firstResponse = self.client.get('/api/orders')
        product= Product.objects.first()
        self.client.post(f'/api/products/{product.id}/add_to_order')
        secondResponse = self.client.get('/api/orders')
        i = 0
        while i < len(firstResponse.data):
            if firstResponse.data[i]["completed_on"] is not None:
                print(f'completed order length: {len(firstResponse.data[i]["products"])} vs {len(secondResponse.data[i]["products"])}')
                self.assertEqual(len(firstResponse.data[i]["products"]),len(secondResponse.data[i]["products"]))
            else:
                print(f'incomplete order length: {len(firstResponse.data[i]["products"])} vs {len(secondResponse.data[i]["products"])}')
                self.assertEqual(len(secondResponse.data[i]["products"]),len(firstResponse.data[i]["products"])+1)
            i = i+1
        self.assertEqual(1,1)
        
