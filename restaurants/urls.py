from django.urls import include, path
from rest_framework.routers import DefaultRouter
from restaurants.views import (
    CompanyViewSet,
    RestaurantViewSet,
    MenuViewSet,
    ModifierViewSet,
    CategoryViewSet,
    ItemViewSet,
    OrderViewSet,
    OrderItemViewSet,
)

app_name = "restaurants"

router = DefaultRouter()

router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"restaurants", RestaurantViewSet, basename="restaurant")
router.register(r"menus", MenuViewSet, basename="menu")
router.register(r"modifiers", ModifierViewSet, basename="modifier")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"items", ItemViewSet, basename="item")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"order-items", OrderItemViewSet, basename="order-item")


urlpatterns = [
    path("", include(router.urls)),
]
