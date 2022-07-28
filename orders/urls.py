from django.urls import path
from orders.views import OrderView, OrderListView

urlpatterns = [
    path('', OrderView.as_view()),
]
