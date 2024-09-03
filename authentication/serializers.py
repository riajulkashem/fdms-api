from rest_framework.serializers import ModelSerializer

from authentication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # write_only means that the password field will not be returned in
        # the response
        extra_kwargs = {"password": {"write_only": True}}


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "address",
        ]
        extra_kwargs = {"password": {"write_only": True}}
