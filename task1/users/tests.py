from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User

# Create your tests here.
class RegisterTest(APITestCase):
    # Test 1: Register user succes
    def test_register_success(self):
        res = self.client.post(
            reverse("register"),
            {
                "phone": "+442738405827",
                "password": "12345678",
                "first_name": "Adi",
                "last_name": "Marim",
            },
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(phone="+442738405827").exists())

class LoginTest(APITestCase):
    def setUp(self):
        User.objects.create_user(
            phone="+442738405827",
            password="12345678",
            first_name="Adi",
            last_name="Marim",
        )

    # Test 2: User login succes
    def test_login_success(self):
        res = self.client.post(
            reverse("login"),
            {
                "phone": "+442738405827",
                "password": "12345678",
            },
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    # Test 3: wrong password is rejected
    def test_login_wrong_password(self):
        res = self.client.post(
            reverse("login"),
            {
                "phone": "+442738405827",
                "password": "wrongpassword",
            },
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)