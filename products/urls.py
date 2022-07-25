
from django.urls import path

from .views import ProductDetailView

urlpatterns = [
    # path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view())
]

    