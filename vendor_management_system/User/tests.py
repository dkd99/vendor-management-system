from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "name": "XYZ Components",
            "contact_details": "sales@xyzcomponents.com\n(456) 789-0123",
            "address": "456 Elm Street, Townsville, State, 67890",
            "password": "NewPassword@123",
            "password2": "NewPassword@123",
            'vendor_code': "Vend001"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="Vend001",
                                             password="NewPassword@123")

    def test_login(self):
        data = {
            "username": "Vend001",
            "password": "NewPassword@123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username="Vend001")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
