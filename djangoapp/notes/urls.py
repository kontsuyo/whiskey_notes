from django.urls import path

from notes import views

urlpatterns = [
    path("", views.TastingNoteList.as_view(), name="tastingnote-list"),
    path(
        "detail/<int:pk>", views.TastingNoteDetail.as_view(), name="tastingnote-detail"
    ),
    path("whiskies", views.WhiskyList.as_view(), name="whiskies-list"),
    path("whisky-detail/<int:pk>", views.WhiskyDetail.as_view(), name="whisky-detail"),
]
