from django.contrib.auth import authenticate, get_user_model
from rest_framework import exceptions, serializers

user_model = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(style={"input_type": "password"})

    def authenticate(self, **kwargs) -> user_model | None:  # type: ignore
        return authenticate(self.context["request"], **kwargs)

    def validate_user(
        self, username: str | None, password: str | None
    ) -> user_model | None:  # type: ignore
        if username and password:
            return self.authenticate(username=username, password=password)
        else:
            msg = 'Must include "username" and "password".'
            raise exceptions.ValidationError(msg)

    @staticmethod
    def validate_auth_user_status(user: user_model) -> None:  # type: ignore
        if not user.is_active:  # type: ignore
            msg = "User account is disabled."
            raise exceptions.ValidationError(msg)

    def validate(self, attrs: dict) -> dict:

        username: str | None = attrs.get("username")
        password: str | None = attrs.get("password")
        user = self.validate_user(username, password)

        if not user:
            msg = "Unable to log in with provided credentials."
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        attrs["user"] = user
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = [
            "username",
            "email",
            "user_type",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "address",
        ]
        # write_only means that the password field will not be returned in
        # the response
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value: str) -> str:
        """
        Check that the password is strong enough.
        """
        has_digit: bool = False
        has_alpha: bool = False
        has_upper: bool = False
        has_special: bool = False
        special_characters: str = "!@#$%^&*()-_=+[]{}|;:,.<>?"

        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )

        for char in value:
            if char.isdigit():
                has_digit = True
            if char.isalpha():
                has_alpha = True
            if char.isupper():
                has_upper = True
            if char in special_characters:
                has_special = True

            # If all conditions are met, no need to continue looping
            if has_digit and has_alpha and has_upper and has_special:
                break

        if not (has_digit and has_alpha and has_upper and has_special):
            errors = []
            if not has_digit:
                errors.append("at least one digit")
            if not has_alpha:
                errors.append("at least one letter")
            if not has_upper:
                errors.append("at least one uppercase letter")
            if not has_special:
                errors.append("at least one special character")

            raise serializers.ValidationError(
                f"Password must contain {', '.join(errors)}."
            )

        return value
