from django.db       import models

from products.models import Product
from users.models    import User

class Order(models.Model):
    order_number = models.CharField(max_length=200)
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order_status = models.ForeignKey('orders.OrderStatus', on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'


class OrderItem(models.Model):
    quantity = models.IntegerField()
    order    = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    product  = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'order_items'


class OrderStatus(models.Model):
    status = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'order_status'