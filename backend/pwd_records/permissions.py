# myapp/permissions.py
from rest_framework import permissions

class IsAdminOrSocialWorkerOrMedicalOfficer(permissions.BasePermission):
    """
    Allow only Admins, Social Workers, and Medical Officers to perform write operations.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            'admin', 'social_worker', 'medical_officer', 'pwd_user'
        ]

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow users to edit only their own records (if applicable), otherwise read-only.
    """
    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
