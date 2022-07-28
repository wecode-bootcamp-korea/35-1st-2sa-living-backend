import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Product
from carts.models    import Cart
from core.utils      import login_confirm

class CartView(View):
    @login_confirm
    def delete(self, request, cart_id):
        user = request.user
        if not Cart.objects.filter(user=user, id=cart_id).exists():
            return JsonResponse({'message':'cart does not exist'}, status=404)
        
        Cart.objects.get(id=cart_id, user=user).delete()
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
            }for cart in Cart.objects.filter(user_id = user.id)
        ]
        return JsonResponse({"carts" : results_cart}, status = 200)

    @login_confirm
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            product_id = data['product_id']
            quantity   = data['quantity']

            MINIMUM_QUANTITY = 1

            if quantity < MINIMUM_QUANTITY:
                return JsonResponse({"message" : "INVALID_QUANTIRY"}, status = 400)

            product = Product.objects.get(id=product_id)

            cart, is_created = Cart.objects.get_or_create(
                user    = user,
                product = product,
                defaults= {
                    "quantity" : quantity
                }
            )
            
            if not is_created:
                cart.quantity += quantity
                cart.save()
            
            status = 201 if is_created else 200
            return JsonResponse({"message" : "Created"}, status = status)

        except KeyError:
            return JsonResponse({"message" : "KeyError"}, status = 400)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "INVALID_PRODUCT"}, status = 400)

        except json.JSONDecodeError:
            return JsonResponse({"message" : "JsonError"}, status = 400)

    @login_confirm
    def get(self, request):
        
        carts = Cart.objects.filter(user_id = request.user.id)

        results_cart = [{
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
            }for cart in carts]

        return JsonResponse({"carts" : results_cart}, status = 200)
