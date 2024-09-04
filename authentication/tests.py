from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class RegistrationViewTests(APITestCase):

    def test_registration(self):
        url = reverse("authentication:register")
        data = {
            "username": "testuser",
            "password": "test@134Pass",
            "user_type": "employee",
            "phone_number": "01700000000",
            "address": "Habiganj Sadar",
        }

        # Test valid data
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

        # Test invalid data
        invalid_data = data.copy()
        invalid_data.pop("username")
        response = self.client.post(url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test existing username
        response = self.client.post(url, data, format="json")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test invalid password
        data["password"] = "test"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Test@1234")
        self.url = reverse("authentication:login")

    def test_login(self):
        # Test valid credentials
        response = self.client.post(
            self.url, {"username": "testuser", "password": "Test@1234"}, format="json"
        )
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], token.key)

        # Test invalid credentials
        response = self.client.post(
            self.url, {"username": "testuser", "password": "wrongpass"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Test@1234")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.url = reverse("authentication:logout")

    def test_logout(self):
        # Test logout with token
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

        # Test logout without token
        self.client.credentials()  # Remove token
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDetailsViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Test@1234")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.url = reverse("authentication:user-detail")

    def test_user_details(self):
        # Test getting user details
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

        # Test updating user details
        new_data = {"username": "newusername", "email": "newemail@example.com"}
        response = self.client.patch(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newusername")
        self.assertEqual(self.user.email, "newemail@example.com")

        # Test accessing without token
        self.client.credentials()  # Remove token
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
