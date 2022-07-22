from django.urls import path

from .views import ProductListView

urlpatterns = [
    path('', ProductListView.as_view()),
    # 127.0.0.1:8000/products?category_id=2
    # 127.0.0.1:8000/products?sub_category_id=7    
]

