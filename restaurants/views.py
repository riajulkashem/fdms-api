from restaurants.models import (
    Company,
    Restaurant,
    Menu,
    Modifier,
    Category,
    Item,
    Order,
    OrderItem,
)
from restaurants.serializers import (
    CompanySerializer,
    RestaurantSerializer,
    MenuSerializer,
    ModifierSerializer,
    CategorySerializer,
    ItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['restaurant']


class ModifierViewSet(ModelViewSet):
    queryset = Modifier.objects.all()
    serializer_class = ModifierSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['menu']


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['menu']


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['category']


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['restaurant']


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['order']
