from django.views.generic import ListView
from .models import Movie, Person


class MovieListView(ListView):
    model = Movie
    context_object_name = "movies"
    paginate_by = 20


class PersonListView(ListView):
    model = Person
    context_object_name = "persons"
    paginate_by = 20
