from django.urls import path
from carts.views import CartView

urlpatterns = [
    path('/cart/<int:cart_id>', CartView.as_view()),
]