from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


class CustomUserManager(UserManager):

    def get_employees(self) -> models.QuerySet:
        return self.filter(user_type="employee")

    def get_customers(self) -> models.QuerySet:
        return self.filter(user_type="customer")

    def get_owners(self) -> models.QuerySet:
        return self.filter(user_type="owner")


class User(AbstractUser):
    RULE_CHOICES = (
        ("owner", "Owner"),
        ("employee", "Employee"),
        ("customer", "Customer"),
    )
    user_type = models.CharField(max_length=10, choices=RULE_CHOICES)
    phone_number = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r"^(?:\+8801|01)?(\d{9})$", message="Invalid Phone Number"
            ),
            MinLengthValidator(limit_value=11),
        ],
    )
    address = models.CharField(max_length=255)
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.get_full_name()
