from django.urls import path
from orders.views import OrderView

urlpatterns = [
    path('/<int:order_id>', OrderView.as_view()),
]

#:8000/orders/1