
from django.urls import path

from .views import ListView, DetailView, CategoryView, SubCategoryView

urlpatterns = [
    path('/category/<int:category_id>', CategoryView.as_view()),
]
