from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


class User(AbstractUser):
    RULE_CHOICES = (
        ("owner", "Owner"),
        ("employee", "Employee"),
        ("client", "Client"),
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

    def __str__(self) -> str:
        return self.get_full_name()
