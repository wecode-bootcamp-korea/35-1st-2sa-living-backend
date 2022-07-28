import uuid

from datetime import datetime
from enum     import Enum

from django.views     import View
from django.http      import JsonResponse
from django.db        import transaction
from django.db.models import Sum,F

from core.utils       import login_confirm
from orders.models    import Order, OrderStatus, OrderItem
from carts.models     import Cart

class OrderView(View):
    @login_confirm
    def get(self, request, order_id):
        user = request.user

        if not Order.objects.filter(id=order_id).exists():
            return JsonResponse({"message" : "Order does not exist"}, status=404)

        order = Order.objects\
                     .annotate(total_price=Sum(F('orderitem__product__price')*F('orderitem__quantity')))\
                     .get(id=order_id)    

        order_list = [{
            'order_id'       : order.id,
            'order_number'   : order.order_number,
            'user_first_name': user.first_name,
            'user_last_name' : user.last_name,
            'order_items'    : [{
                'product_id'           : order_item.product.id,
                'quantity'             : order_item.quantity,
                'furniture_korean_name': order_item.product.furniture.korean_name,
                'product_image'        : order_item.product.thumbnail_image_url,
                'price'                : int((order_item.quantity) * (order_item.product.price))
            } for order_item in order.orderitem_set.all()],
            'total_price' : int(order.total_price)
        }]
        
        return JsonResponse({'order_list':order_list}, status=200)
