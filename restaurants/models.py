import uuid
from typing import Any

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(TimeStampedModel):
    """
    A model representing a company.

    Attributes:
    -----------
        name: The name of the company.
        description: A description of the company.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Restaurant(TimeStampedModel):
    """
    A model representing a restaurant.

    Attributes:
    -----------
        company: A foreign key to the Company model, representing the company that owns
        the restaurant.
        owner: A foreign key to the User model, representing the owner of the
        restaurant.
        name: A character field with a maximum length of 255 characters, representing
        the name of the restaurant. It must be unique.
        description: A text field, representing a description of the restaurant.
        phone_number: A character field with a maximum length of 20 characters,
        representing the phone number of the restaurant.
        email: An email field, representing the email address of the restaurant.
        website: A URL field, representing the website of the restaurant.
        address: A character field with a maximum length of 255 characters,
        representing the address of the restaurant.
    """

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="restaurants"
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="restaurants"
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Menu(TimeStampedModel):
    """
    A model representing a menu for a restaurant.

    Attributes:
    -----------
    restaurant: A foreign key to the Restaurant model, representing the restaurant
    that the menu belongs to.
    name: A character field with a maximum length of 255 characters, representing
    the name of the menu.
    description: A text field, representing a description of the menu.
    """

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.restaurant.name}"


class Modifier(TimeStampedModel):
    """
    A model representing a modifier for a menu item.

    Attributes:
    -----------
    name: A character field with a maximum length of 255 characters, representing
    the name of the modifier.
    price: A decimal field with a maximum of 10 digits and 2 decimal places,
    representing the price of the modifier.
    It must be greater than or equal to 0.
    is_available: A boolean field, representing whether the modifier is currently
    available. It defaults to True.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Category(TimeStampedModel):
    """
    A model representing a category for menu items.

    Attributes:
    -----------
    restaurant: A foreign key to the Restaurant model, representing the restaurant
    that the category belongs to.
    name: A character field with a maximum length of 255 characters, representing
    the name of the category.
    description: A text field, representing a description of the category.
    """

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Item(TimeStampedModel):
    """
    A model representing a menu item.
    Attributes:
    -----------
    menu: A foreign key to the Menu model, representing the menu that
    the item belongs to.
    category: A foreign key to the Category model, representing the category
    that the item belongs to.
    name: A character field with a maximum length of 255 characters, representing
    the name of the item.
    description: A text field, representing a description of the item.
    price: A decimal field with a maximum of 10 digits and 2 decimal places,
    representing the price of the item. It must be greater than or equal to 0.
    is_available: A boolean field, representing whether the item is currently available.
    It defaults to True.
    modifiers: A many-to-many relationship with the Modifier model, representing the
    modifiers that can be added to the item. It is blank by default.
    """

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
    modifiers = models.ManyToManyField(Modifier, related_name="items", blank=True)

    def __str__(self) -> str:
        return self.name


class Order(TimeStampedModel):
    """
    A model representing an order placed by a client for a restaurant.

    Attributes:
    -----------
    order_id: A character field with a maximum length of 20 characters, representing
    a unique identifier for the order.
    It is automatically generated when the order is created and is not editable.
    client: A foreign key to the User model, representing the client who placed
    the order.
    restaurant: A foreign key to the Restaurant model, representing the restaurant
    that the order is for.
    address: A character field with a maximum length of 500 characters, representing
    the delivery address for the order.
    items: A many-to-many relationship with the Item model, representing the items
    that were ordered.
    The relationship is defined through the OrderItem model.
    total_amount: A decimal field with a maximum of 10 digits and 2 decimal places,
    representing the total amount of the order.
    It must be greater than or equal to 0.
    payment_method: A character field with a maximum length of 4 characters,
    representing the payment method used for the order.
    It can be either "card" or "cash".
    is_paid: A boolean field, representing whether the order has been paid for.
    It defaults to False.
    """

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


class OrderItem(TimeStampedModel):
    """
    A model representing an item in an order.

    Attributes:
    -----------
    order: A foreign key to the Order model, representing the order that the
    item belongs to.
    item: A foreign key to the Item model, representing the item that was ordered.
    quantity: A positive integer field, representing the quantity of the item that
    was ordered.
    It must be greater than or equal to 1.
    price: A decimal field with a maximum of 10 digits and 2 decimal places,
    representing the price of the item.
    It must be greater than or equal to 0.
    modifiers: A many-to-many relationship with the Modifier model, representing
    the modifiers that
    were added to the item. It is blank by default.
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    modifiers = models.ManyToManyField(Modifier, related_name="order_items", blank=True)

    def __str__(self) -> str:
        return f"{self.quantity} x {self.item.name} - Order {self.order.order_id}"
