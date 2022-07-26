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
    def post(self, request, *args, **kwargs):
        user  = request.user
        carts = Cart.objects.filter(user_id = request.user.id)
        if not carts.exists():
            return JsonResponse({"message" : "NOT EXIST CARTS"}, status=400)

        with transaction.atomic():
            order_number = uuid.uuid4()
            order_status = OrderStatus.objects.get(status="결제완료")
            order = Order.objects.create(
                user         = user,
                order_number = order_number,
                order_status = order_status,
            )
            order_items	 = [OrderItem(
                order    = order,
                product  = cart.product,
                quantity = cart.quantity
            ) for cart in carts]
            carts.delete()
            OrderItem.objects.bulk_create(order_items)


        items = OrderItem.objects.filter(order_id = order.id)
        results_order_items = []

        for item in items:
            results_order_items.append(
                {
                    "order_id"                    : item.id,
                    "order_image"                 : item.product.thumbnail_image_url,
                    "user_firstname"              : item.order.user.first_name,
                    "user_lastname"               : item.order.user.last_name,
                    "furniture_korean_name"       : item.product.furniture.korean_name,
                    "furniture_english_name"      : item.product.furniture.english_name,
                    "furniture_brand"             : item.product.furniture.brand.name,
                    "furniture_color_korean_name" : item.product.color.korean_name,
                    "furniture_color_english_name": item.product.color.english_name,
                    "price"                       : item.product.price,
                    "quantity"                    : item.quantity,
                }
            )
        return JsonResponse({"order_items" : results_order_items}, status = 200)
