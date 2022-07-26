import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Product
from carts.models    import Cart
from core.utils      import login_confirm

class CartView(View):
    @login_confirm
    def delete(self, request, cart_id):
        if Cart.objects.filter(user=request.user, id=cart_id).delete()[0]:
            carts = Cart.objects.filter(user_id = request.user.id)
            results_cart = [
                {
                    "cart_id"                     : cart.id,
                    "cart_image"                  : cart.product.thumbnail_image_url,
                    "user_firstname"              : cart.user.first_name,
                    "user_lastname"               : cart.user.last_name,
                    "furniture_korean_name"       : cart.product.furniture.korean_name,
                    "furniture_english_name"      : cart.product.furniture.english_name,
                    "furniture_brand"             : cart.product.furniture.brand.name,
                    "furniture_color_korean_name" : cart.product.color.korean_name,
                    "furniture_color_english_name": cart.product.color.english_name,
                    "price"                       : cart.product.price,
                    "quantity"                    : cart.quantity,
                }for cart in carts
            ]
            return JsonResponse({"carts" : results_cart}, status = 200)
        return JsonResponse({'message':'fail'}, status=400)