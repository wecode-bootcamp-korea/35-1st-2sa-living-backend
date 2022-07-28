import uuid

from datetime         import datetime
from django.views     import View
from django.http      import JsonResponse
from django.db        import transaction
from django.db.models import Sum,F

from core.utils       import login_confirm
from orders.models    import Order, OrderStatus, OrderItem
from carts.models     import Cart

class OrderListView(View):
    @login_confirm
    def get(self, request):
        user   = request.user
        orders = Order.objects\
                      .annotate(total_price=Sum(F('product__price')*F('quantity')))\
                      .filter(user=user)
        
        order_list=[
            {
                "order_id"     : order.id,
                "order_number" : order.order_number,
                "order_status" : order.order_status.status,
                "total_price"  : order.total_price,
                'created_at'   : order.created_at.strftime("%Y년 %m월 %d일 %H:%M"),
                'updated_at'   : order.updated_at.strftime("%Y년 %m월 %d일 %H:%M"),

            } for order in orders
        ]
        return JsonResponse({"result": order_list}, status=200)
