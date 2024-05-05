from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from vendor.models import Vendor as vendor_
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


# class RegisterTestCase(APITestCase):

#     def test_register(self):
#         data = {
#             "name": "XYZ Components",
#             "contact_details": "sales@xyzcomponents.com\n(456) 789-0123",
#             "address": "456 Elm Street, Townsville, State, 67890",
#             "password": "NewPassword@123",
#             "password2": "NewPassword@123",
#             'vendor_code': "Vend001"
#         }
#         response = self.client.post(reverse('register'), data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class Vendor(APITestCase):

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
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_vendor_create(self):
        data = {
        "name": "XYZ Components",
        "contact_details": "sales@xyzcomponents.com\n(456) 789-0123",
        "address": "456 Elm Street, Townsville, State, 67890",
        "vendor_code": "VEND001",
        "on_time_delivery_rate": 0.6799999999999999,
        "quality_rating_avg": 0.0,
        "average_response_time": 2880.0,
        "fulfillment_rate": 0.0
        }

        response = self.client.post(reverse('vendor-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_vendor_list(self):
        response = self.client.get(reverse('vendor-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_vendor_put(self):
        data = {
        "name": "XYZ Components",
        "contact_details": "sales@xyzcomponents.com\n(456) 789-0123",
        "address": "456 Elm Street, Townsville, State, 67890",
        "vendor_code": "VEND001",
        "on_time_delivery_rate": 0.6799999999999999,
        "quality_rating_avg": 0.0,
        "average_response_time": 2880.0,
        "fulfillment_rate": 0.0
        }

        response = self.client.put(reverse('vendor-retrieve-update-destroy', args=(self.vendor.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_vendor_get(self):
        response = self.client.get(reverse('vendor-retrieve-update-destroy', args=(self.vendor.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)        

    def test_vendor_delete(self):
        response = self.client.delete(reverse('vendor-retrieve-update-destroy', args=(self.vendor.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)         