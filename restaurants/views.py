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


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsOwnerOrEmployeeOrReadOnly]
    filterset_fields = ["restaurant"]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrEmployeeOrReadOnly]
    filterset_fields = ["menu"]


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsOwnerOrEmployeeOrReadOnly]
    filterset_fields = ["category"]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["restaurant"]


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["order"]
