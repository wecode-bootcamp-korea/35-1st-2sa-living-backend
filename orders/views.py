import uuid
from datetime		 import datetime
from django.views    	 import View
from django.http     	 import JsonResponse
from django.db       	 import transaction
from django.db.models	 import Sum,F
from core.utils     	 import login_confirm
from orders.models   	 import Order, OrderItem, OrderStatus
from carts.models    	 import Cart

class OrderView(View):
    @login_confirm
    def get(self, request, *args, **kwargs):
        user        = request.user
        orders      = Order.objects.filter(user=user)
        order_items = OrderItem.objects.filter(order__in=orders)
        total_price = order_items.aggregate(total_price=Sum(F('product__price')*F('quantity')))['total_price']
        order_item_list = [{
            'order_item_id'         : order_item.id,
            'furniture_korean_name' : order_item.product.furniture.korean_name,
            'furniture_english_name': order_item.product.furniture.english_name,
            'product_image'         : order_item.product.thumbnail_image_url,
            'product_korean_color'  : order_item.product.color.korean_name,
            'product_english_color' : order_item.product.color.english_name,
            'quantity'              : order_item.quantity,
            'price'		    : int(order_item.product.price * order_item.quantity),
            'created_at'            : order_item.order.created_at.strftime("%Y년 %m월 %d일 %H:%M"),
            'updated_at'            : order_item.order.updated_at.strftime("%Y년 %m월 %d일 %H:%M"),
        }for order_item in order_items]
        order_list = [{
            'order_id'       : order.id,
            'order_number'   : order.order_number,
            'user_first_name': user.first_name,
            'user_last_name' : user.last_name,
            'order_items'    : order_item_list,
            'total_price'    : int(total_price),
            'order_status'   : order.order_status.status,
        }for order in orders]
        return JsonResponse({"result" : order_list}, status=200)
