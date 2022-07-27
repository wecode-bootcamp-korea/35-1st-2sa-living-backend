import uuid

from datetime         import datetime
from django.views     import View
from django.http      import JsonResponse
from django.db        import transaction
from django.db.models import Sum,F

from core.utils       import login_confirm
from orders.models    import Order, OrderStatus, OrderItem
from carts.models     import Cart
from users.models     import User

class OrderView(View):
    @login_confirm
    def get(self, request):
        user        = request.user
        order       = request.GET.get('order_id')
        order_items = Order.objects.get(id=order).orderitem_set.all()
        total_price = int(Order.objects.filter(id=order).annotate(total=Sum(F('orderitem__product__price')*F('orderitem__quantity')))[0].total)
    
        order_list = [{
            'order_id'       : order,
            'user_first_name': User.objects.get(id=user.id).first_name,
            'user_last_name' : User.objects.get(id=user.id).last_name,
            'order_items'    : [{
                'product_id'           : order_item.product.id,
                'quantity'             : order_item.quantity,
                'furniture_korean_name': order_item.product.furniture.korean_name,
                'product_image'        : order_item.product.thumbnail_image_url,
                'price'                : int((order_item.quantity) * (order_item.product.price))
            } for order_item in order_items],
            'total_price' : total_price
        }]
        
        return JsonResponse({'order_list':order_list}, status=200)
