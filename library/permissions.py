from rest_framework import permissions


class BaseObjectAccessPermission(permissions.BasePermission):
    message = 'You can only read data, not edit'

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return request.method in permissions.SAFE_METHODS


class ReaderAccessPermission(permissions.BasePermission):
    message = 'You can only work with your Reader'

    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return True
        if request.user and request.user.is_staff:
            return True
        return request.user == obj.user
