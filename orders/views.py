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


class OrderStatus(Enum):
    PAYED    = 1
    PREPARED = 2
    SHIPPING = 3

class OrderView(View):

    @login_confirm
    def post(self, request, *args, **kwargs):
        user  = request.user
        carts = Cart.objects.filter(user = request.user)
        
        if not carts.exists():
            return JsonResponse({"message" : "NOT EXIST CARTS"}, status=404)

        with transaction.atomic():
            order = Order.objects.create(
                user            = user,
                order_number    = uuid.uuid4(),
                order_status_id = OrderStatus.PAYED.value,
            )

            order_items = [
                OrderItem(
                    order    = order,
                    product  = cart.product,
                    quantity = cart.quantity
                ) for cart in carts
            ]
            carts.delete()
            OrderItem.objects.bulk_create(order_items)

        result = {
                "order_id"       : order.id,
                "order_number"   : order.order_number,
                "user_firstname" : order.user.first_name,
                "user_lastname"  : order.user.last_name,
                "order_items"    : [{
                    "order_image"                 : item.product.thumbnail_image_url,
                    "furniture_korean_name"       : item.product.furniture.korean_name,
                    "furniture_english_name"      : item.product.furniture.english_name,
                    "furniture_brand"             : item.product.furniture.brand.name,
                    "furniture_color_korean_name" : item.product.color.korean_name,
                    "furniture_color_english_name": item.product.color.english_name,
                    "price"                       : item.product.price,
                    "quantity"                    : item.quantity,
                }for item in order.orderitem_set.all()]
            }
                
        return JsonResponse({"order_items" : result}, status = 200)
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
