import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Product
from carts.models    import Cart
from core.utils      import LoginConfirm

class CartView(View):

    @LoginConfirm
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