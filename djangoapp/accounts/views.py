from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from accounts.serializers import CustomUserSerializer

User = get_user_model()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class CreateUser(generics.CreateAPIView):
    model = User
    serializer_class = CustomUserSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
