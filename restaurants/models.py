import uuid
from typing import Any

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from authentication.models import Owner

User = get_user_model()


class OperationLogModel(models.Model):
    """
    An abstract base class model that provides self-updating
    common fields.
    """

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="creator_%(class)s_objects",
        editable=False,
        verbose_name="Created by",
        help_text="The user who created this object.",
    )

    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updater_%(class)s_objects",
        editable=False,
        verbose_name="Updated by",
        help_text="The user who last updated this object.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(OperationLogModel):

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Restaurant(OperationLogModel):

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="restaurants"
    )
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name="restaurants"
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Menu(OperationLogModel):

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.restaurant.name}"


class Category(OperationLogModel):

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Item(OperationLogModel):

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="items"
    )
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Order(OperationLogModel):

    PAYMENT_METHODS = [("card", "Card"), ("cash", "Cash")]

    order_id = models.CharField(max_length=20, unique=True, editable=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="orders"
    )
    address = models.CharField(max_length=500)
    items = models.ManyToManyField(Item, through="OrderItem")
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHODS)
    is_paid = models.BooleanField(default=False)

    def generate_order_id(self) -> str:
        prefix = "ORD"
        restaurant_code = "".join(
            [word[0].upper() for word in self.restaurant.name.split()]
        )
        unique_code = str(uuid.uuid4()).split("-")[0].upper()
        return f"{prefix}-{restaurant_code}-{unique_code}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Order {self.order_id} - {self.client.get_full_name()}"


class OrderItem(OperationLogModel):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    def __str__(self) -> str:
        return f"{self.quantity} x {self.item.name} - Order {self.order.order_id}"
