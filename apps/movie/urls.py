from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path("", views.MovieListView.as_view(), name="movie-list"),
    path("persons/", views.PersonListView.as_view(), name="person-list"),
]
