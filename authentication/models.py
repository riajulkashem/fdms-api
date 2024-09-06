from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        return self.user.get_full_name()


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    designation = models.CharField(max_length=255)
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
    )

    def __str__(self) -> str:
        return self.user.get_full_name()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        return self.user.get_full_name()


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):  # type: ignore
    # Create a profile for the user when a new user is created.
    if created:
        if instance.user_type == "customer":
            Customer.objects.create(user=instance)
        elif instance.user_type == "employee":
            Employee.objects.create(user=instance)
        elif instance.user_type == "owner":
            Owner.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_profile(sender, instance, **kwargs):  # type: ignore
    # Ensure that profile data is saved when the user is saved
    if instance.user_type == "customer" and hasattr(instance, "customer"):
        instance.customer.save()
    elif instance.user_type == "employee" and hasattr(instance, "employee"):
        instance.employee.save()
    elif instance.user_type == "owner" and hasattr(instance, "owner"):
        instance.owner.save()
