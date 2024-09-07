from typing import Any

from rest_framework import serializers

from restaurants.models import (
    Category,
    Company,
    Item,
    Menu,
    Order,
    OrderItem,
    Restaurant,
)


class CustomModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data: Any) -> Any:
        # Create the instance
        instance = super().create(validated_data)

        # Update the instance with the created_by field
        instance.created_by = self.context["request"].user
        instance.save()

        return instance

    def update(self, instance: Any, validated_data: Any) -> Any:
        # Update the instance with the updated_by field
        instance.last_updated_by = self.context["request"].user
        return super().update(instance, validated_data)


class CompanySerializer(CustomModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class RestaurantSerializer(CustomModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuSerializer(CustomModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class CategorySerializer(CustomModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemSerializer(CustomModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class OrderSerializer(CustomModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(CustomModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
