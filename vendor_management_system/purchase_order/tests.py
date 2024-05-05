from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from vendor.models import Vendor as vendor_
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from rest_framework.authtoken.models import Token
import json


class PurchaseOrderTests(APITestCase):

    def setUp(self):
        data = {
            "name": "XYZ Components",
            "contact_details": "sales@xyzcomponents.com\n(456) 789-0123",
            "address": "456 Elm Street, Townsville, State, 67890",
            "password": "NewPassword@123",
            "password2": "NewPassword@123",
            'vendor_code': "Vend001"
        }
        response = self.client.post(reverse('register'), data)
        self.user = User.objects.get(username= data.get('vendor_code'))
        self.vendor = vendor_.objects.get(vendor_code=self.user.username)
        self.token = Token.objects.get(user__username="Vend001")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', is_staff=True)
        self.admin_token, created = Token.objects.get_or_create(user=self.admin_user)
        self.client_admin = APIClient()
        self.client_admin.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        
    def test_purchase_order_post(self):

        data =     {
        "po_number": "PO001",
        "order_date": "2024-04-01T08:00:00Z",
        "delivery_date": "2024-04-15T08:00:00Z",
        "items": json.dumps([
            {
                "name": "Laptop",
                "description": "15-inch laptop with SSD",
                "unit_price": 1200.0
            },
            {
                "name": "Monitor",
                "description": "27-inch 4K monitor",
                "unit_price": 600.0
            }
        ]),
        "quantity": 10,
        "status": "pending",
        "quality_rating": 4.8,
        "issue_date": "2024-04-20T08:00:00Z",
        "vendor": self.vendor.vendor_code
        }
        print(vendor_.objects.all(),self.vendor.vendor_code,"====================>>>>>")
        response = self.client.post(reverse('purchase-order-list-create'), data)
        print(response.content,"888888888888")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_purchase_order_get(self):
        response = self.client.get(reverse('purchase-order-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_purchase_order_post_admin(self):
        # Log in as the admin user
        res = self.client.force_login(self.admin_user)

        # Define the purchase order data
        data = {
            "po_number": "PO008",
            "order_date": "2024-04-01T08:00:00Z",
            "delivery_date": "2024-04-15T08:00:00Z",
            "items": json.dumps([
                {
                    "name": "Laptop",
                    "description": "15-inch laptop with SSD",
                    "unit_price": 1200.0
                },
                {
                    "name": "Monitor",
                    "description": "27-inch 4K monitor",
                    "unit_price": 600.0
                }
            ])
            ,
            "quantity": 10,
            "status": "pending",
            "quality_rating": 4.8,
            "issue_date": "2024-04-20T08:00:00Z","acknowledgment_date": "" ,"vendor": self.vendor.vendor_code
        }

        # Make the POST request to create the purchase order
        response = self.client_admin.post(reverse('purchase-order-list-create'), data)
        self.response_data = json.loads(response.content.decode('utf-8'))
        print(self.response_data['id'])

        # Ensure that the admin user can create purchase orders
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class PurchaseOrderGetPutTests(APITestCase):

    def setUp(self):
        data = {
            "name": "XYZ Components",
            "contact_details": "sales@xyzcomponents.com\n(456) 789-0123",
            "address": "456 Elm Street, Townsville, State, 67890",
            "password": "NewPassword@123",
            "password2": "NewPassword@123",
            'vendor_code': "Vend001"
        }
        response = self.client.post(reverse('register'), data)
        self.user = User.objects.get(username= data.get('vendor_code'))
        self.vendor = vendor_.objects.get(vendor_code=self.user.username)
        self.token = Token.objects.get(user__username="Vend001")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', is_staff=True)
        self.admin_token, created = Token.objects.get_or_create(user=self.admin_user)
        self.client_admin = APIClient()
        self.client_admin.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        res = self.client.force_login(self.admin_user)

        # Define the purchase order data
        data = {
            "po_number": "PO008",
            "order_date": "2024-04-01T08:00:00Z",
            "delivery_date": "2024-04-15T08:00:00Z",
            "items": json.dumps([
                {
                    "name": "Laptop",
                    "description": "15-inch laptop with SSD",
                    "unit_price": 1200.0
                },
                {
                    "name": "Monitor",
                    "description": "27-inch 4K monitor",
                    "unit_price": 600.0
                }
            ])
            ,
            "quantity": 10,
            "status": "pending",
            "quality_rating": 4.8,
            "issue_date": "2024-04-20T08:00:00Z","acknowledgment_date": "" ,"vendor": self.vendor.vendor_code
        }

        # Make the POST request to create the purchase order
        response = self.client_admin.post(reverse('purchase-order-list-create'), data)
        self.response_data = json.loads(response.content.decode('utf-8'))
        
        print(self.response_data,type(self.response_data.get("vendor")))
        
    def test_purchase_order_get_admin(self):
        response = self.client.get(reverse('purchase-order-retrieve-update-destroy',args=(self.response_data['id'],)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)        

    def test_vendor_put(self):
        data = {
            "id" : 1,
            "po_number": "PO008",
            "order_date": "2024-04-01T08:00:00Z",
            "delivery_date": "2024-04-15T08:00:00Z",
            "items": json.dumps([
                {
                    "name": "Laptop",
                    "description": "15-inch laptop with SSD",
                    "unit_price": 1200.0
                },
                {
                    "name": "Monitor",
                    "description": "27-inch 4K monitor",
                    "unit_price": 600.0
                }
            ])
            ,
            "quantity": 10,
            "status": "completed",
            "quality_rating": 4.8,
            "issue_date": "2024-04-20T08:00:00Z","acknowledgment_date": "" ,"vendor": self.vendor.vendor_code
        }
        

        response = self.client.put(reverse('purchase-order-retrieve-update-destroy', args=(self.response_data['id'],)),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_delete(self):
        response = self.client.delete(reverse('purchase-order-retrieve-update-destroy', args=(self.response_data['id'],)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
