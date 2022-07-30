from rest_framework import permissions


class IsLoginUser(permissions.BasePermission):

    def has_permission(self, request, view):
        print('1111111111111111111111111111')
        return request.user and request.user.is_authenticated
