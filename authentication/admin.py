from django.contrib import admin

from authentication.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "date_joined")
    # Add this line to exclude the password field from the list view
    exclude = ("password",)
    # Add this line to exclude the password field from the add/change view
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
            },
        ),
    )


admin.site.register(User, UserAdmin)
