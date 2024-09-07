from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import User
from restaurants.models import Company


class CompanyViewSetTest(APITestCase):

    def setUp(self) -> None:
        self.owner_user = User.objects.create_user(
            username="owner", password="password", user_type="owner"
        )
        self.non_owner_user = User.objects.create_user(
            username="non_owner", password="password", user_type="employee"
        )
        self.company = Company.objects.create(
            name="Test Company", created_by=self.owner_user
        )
        self.client.force_authenticate(user=self.owner_user)

    def test_create_company(self) -> None:
        # Test creating a new company as an owner user.
        url = reverse("restaurants:company-list")
        data = {"name": "New Company", "description": "A new company"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_create_company(self) -> None:
        # Test creating a new company as a non-owner user.
        self.client.force_authenticate(user=None)
        url = reverse("restaurants:company-list")
        data = {"name": "New Company"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_company(self) -> None:
        # Test updating a company as an owner user.
        url = reverse("restaurants:company-detail", kwargs={"pk": self.company.pk})
        data = {"name": "Updated Company"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Company")

    def test_unauthorized_update_company(self) -> None:
        # Test updating a company as a non-owner user.
        self.client.force_authenticate(user=self.non_owner_user)
        url = reverse("restaurants:company-detail", kwargs={"pk": self.company.pk})
        data = {"name": "Updated Company"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_company(self) -> None:
        url = reverse("restaurants:company-detail", kwargs={"pk": self.company.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
