from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Checkout, UserProfile
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class IsAllowed(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated


class OnlyLibrarian(BasePermission):
    def has_permission(self, request, view):
        # if request.user.isLibrarian:
        #     return True
        print(request.user.isLibrarian)
        return request.user.isLibrarian