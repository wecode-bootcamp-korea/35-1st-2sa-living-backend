from django.urls import path
from orders.views import OrderView, OrderListView

urlpatterns = [
    path('/list', OrderListView.as_view()),
]
