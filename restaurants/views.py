from typing import Any

from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authentication.permissions import IsOwner, IsOwnerOrEmployeeOrReadOnly
from restaurants.models import (
    Category,
    Company,
    Item,
    Menu,
    Order,
    OrderItem,
    Restaurant,
)
from restaurants.serializers import (
    CategorySerializer,
    CompanySerializer,
    ItemSerializer,
    MenuSerializer,
    OrderItemSerializer,
    OrderSerializer,
    RestaurantSerializer,
)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsOwner]


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwner]

    def get_queryset(self) -> QuerySet | None:
        user: Any = self.request.user
        if user.user_type == "owner":
            return self.queryset.filter(owner=user)
        return self.queryset.none()


class CustomViewSetForEmployee(ModelViewSet):
    permission_classes = [IsOwnerOrEmployeeOrReadOnly]

    def get_queryset(self) -> QuerySet | None:
        user: Any = self.request.user
        if user.user_type == "owner":
            return self.queryset.filter(owner=user)  # type: ignore
        elif user.user_type == "employee":
            return self.queryset.filter(employees=user)  # type: ignore
        return self.queryset.none()  # type: ignore


class MenuViewSet(CustomViewSetForEmployee):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsOwnerOrEmployeeOrReadOnly]


class CategoryViewSet(CustomViewSetForEmployee):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrEmployeeOrReadOnly]


class ItemViewSet(CustomViewSetForEmployee):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsOwnerOrEmployeeOrReadOnly]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
