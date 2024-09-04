from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import (
    LoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


class RegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def login(self) -> Token:
        self.user = self.serializer.validated_data["user"]
        self.token, _ = Token.objects.get_or_create(user=self.user)
        return self.token

    def get_response(self) -> Response:
        serializer = UserSerializer(self.user)
        response_data: Any = serializer.data
        response_data["token"] = self.token.key
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> Response:  # type: ignore
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


class LogoutView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs) -> Response:  # type: ignore
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK,
        )


class UserDetailsView(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user
