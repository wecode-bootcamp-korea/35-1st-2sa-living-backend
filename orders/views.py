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

class OrderListView(View):
    @login_confirm
    def get(self, request):
        user   = request.user
        orders = Order.objects.filter(user_id = user.id)
        
        order_list=[
            {
                "order_id"    : order.id,
                "order_number": order.order_number,
                "order_status": order.order_status.status,
                "total_price" : OrderItem.objects.filter(order=order).aggregate(total=Sum(F('product__price')*F('quantity')))['total'],
                'created_at'  : order.created_at.strftime("%Y년 %m월 %d일 %H:%M"),
                'updated_at'  : order.updated_at.strftime("%Y년 %m월 %d일 %H:%M"),

            } for order in orders
        ]
        return JsonResponse({"result": order_list}, status=200)
