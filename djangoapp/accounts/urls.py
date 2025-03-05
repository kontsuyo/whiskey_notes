from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from accounts import views

urlpatterns = [
    path("", views.UserList.as_view(), name="user-list"),
    path("detail/<int:pk>", views.UserDetail.as_view(), name="user-detail"),
    path("register/", views.CreateUser.as_view(), name="register-user"),
    path("api-token-auth/", obtain_auth_token, name="auth-token"),
]
