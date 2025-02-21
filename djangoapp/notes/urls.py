from django.urls import path

from notes import views

urlpatterns = [
    path("", views.WhiskeyList.as_view(), name="whiskey-list"),
    path("detail/<int:pk>", views.WhiskeyDetail.as_view(), name="whiskey-detail"),
]
