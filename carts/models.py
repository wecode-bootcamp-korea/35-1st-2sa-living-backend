from django.db       import models
from products.models import Product
from users.models    import User

class Cart (models.Model):
    count      = models.IntegerField()
    user_id    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product_id = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'