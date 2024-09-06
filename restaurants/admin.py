from django.contrib import admin

from restaurants.models import (
    Category,
    Company,
    Item,
    Menu,
    Modifier,
    Order,
    OrderItem,
    Restaurant,
)

admin.site.register(Category)
admin.site.register(Company)
admin.site.register(Item)
admin.site.register(Menu)
admin.site.register(Modifier)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Restaurant)
