from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.api import serializers
from accounts import models
from core.infrastructure import choices
from core.infrastructure.check_permissions import ProfilePermissions


class RegisterUserView(viewsets.ModelViewSet):
    """API Views for Registering Users in the System"""
    
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]
    
    def perform_create(self, serializer):
        serializer.save(role=choices.CUSTOMER)


class RegisterStaffView(viewsets.ModelViewSet):
    """API Views for Registering Staffs in the System"""
    
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]
    
    def perform_create(self, serializer):
        serializer.save(role=choices.STAFF)


class UserProfileView(viewsets.ModelViewSet):
    """API Views for Handling User Profile in the System"""   
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, ProfilePermissions,)
    http_method_names = ["get","put","patch","delete"]
    
    def get_queryset(self):
        return models.User.objects.filter(email=self.request.user.email)
