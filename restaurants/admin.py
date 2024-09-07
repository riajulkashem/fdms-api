from django.contrib import admin

from restaurants.models import (
    Category,
    Company,
    Item,
    Menu,
    Order,
    OrderItem,
    Restaurant,
)

admin.site.register(Category)
admin.site.register(Company)
admin.site.register(Item)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Restaurant)
