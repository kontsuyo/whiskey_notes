from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import CustomUserSerializer, RegisterSerializer

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


class RegisterView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        """
        Register a new user.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {
                        "user": serializer.data,
                        "message": "User created successfully",
                    },
                    status=status.HTTP_201_CREATED,
                )
            except ValidationError as e:
                return Response(
                    {"error": e.detail},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except IntegrityError:
                return Response(
                    {"error": "Database integrity error"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
