from django.urls import path

from accounts import views

urlpatterns = [
    path("", views.UserList.as_view(), name="user-list"),
    path("register/", views.UserRegisterView.as_view(), name="register-user"),
    path("login/", views.LoginView.as_view(), name="login-user"),
    path("logout/", views.LogoutView.as_view(), name="logout-user"),
    path("<str:username>/", views.UserDetailView.as_view(), name="user-detail"),
    path("<str:username>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path(
        "<str:username>/delete/", views.CloseAccountView.as_view(), name="user-delete"
    ),
]
