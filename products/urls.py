
from django.urls import path

from .views import ListView, DetailView

urlpatterns = [
    path('/list', ListView.as_view()),
    path('/detail', DetailView.as_view())
]
