from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        # only allowed to the user with usertype is "owner" | object creator
        if request.user.user_type == "woner" or request.user == obj.user:
            return True
        return False


class IsOwnerOrEmployeeOrReadOnly(permissions.BasePermission):

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # if the user is superuser
        if request.user.is_superuser:
            return True

        # creator of the object
        if request.user == obj.user:
            return True

        # allowed for the user, usertype is "owner" and owner of the related restaurant
        if (
            request.user.user_type == "owner"
            and hasattr(obj, "restaurant")
            and request.user.owner == obj.restaurant.owner
        ):
            return True

        # usertype is "employee" and employee of the related restaurant
        if (
            request.user.user_type == "employee"
            and hasattr(obj, "restaurant")
            and request.user.employee.restaurant == obj.restaurant
        ):
            return True

        return False
