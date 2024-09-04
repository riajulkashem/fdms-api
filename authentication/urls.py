from django.urls import path

from authentication.views import (
    LoginView,
    LogoutView,
    RegistrationView,
    UserDetailsView,
)

app_name = "authentication"

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user-detail/", UserDetailsView.as_view(), name="user-detail"),
]
