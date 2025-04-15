from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import (
    CustomUserSerializer,
    RegisterSerializer,
    UserUpdateSerializer,
)

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


from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]  # type: ignore
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Logout a user by deleting their authentication token.
        """
        request.user.auth_token.delete()
        return Response(
            {"message": "User logged out successfully"}, status=status.HTTP_200_OK
        )


class UserUpdateView(APIView):
    def patch(self, request, username):
        """
        Update a user's details.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
