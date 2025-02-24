from django.urls import path

from accounts import views

urlpatterns = [
    path("", views.UserList.as_view(), name="user-list"),
    path("detail/<int:pk>", views.UserDetail.as_view(), name="user-detail"),
    path("register/", views.CreateUser.as_view(), name="register-user"),
]
