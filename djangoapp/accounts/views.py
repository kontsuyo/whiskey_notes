from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
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


class UserRegisterView(APIView):

    def post(self, request, *args, **kwargs):
        """
        Register a new user.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "user": serializer.data,
                    "message": "User created successfully",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class UserDetailView(APIView):
    def get(self, request, username):
        """
        Retrieve a user's details.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        response_data = {
            "message": "User details retrieved successfully",
            "user": {"username": user.username},
        }
        return Response(response_data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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

        # ユーザー自身のみが情報を更新可能
        if request.user != user:
            return Response(
                {"error": "You do not have permission to update this user's details."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, username):
        """
        Delete a user's account.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # ユーザー自身のみがアカウントを削除可能
        if request.user != user:
            return Response(
                {"error": "You do not have permission to delete this user's account."},
                status=status.HTTP_403_FORBIDDEN,
            )

        user.delete()
        return Response(
            {"message": "User account deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
