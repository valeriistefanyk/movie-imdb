from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.index, name='home'),
]