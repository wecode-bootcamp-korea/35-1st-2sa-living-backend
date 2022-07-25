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
            data      = json.loads(request.body)
            product   = Product.objects.get(id = data['product_id'])
            user      = request.user
            quantity = data['quantity']

            if not Cart.objects.filter(product=product,user=user).exists():
                Cart.objects.create(
                    user     = user,
                    product  = product,
                    quantity = quantity
                )
            else:
                temp = Cart.objects.filter(product=product, user=user)[0].quantity
                print(Cart.objects.filter(product=product, user=user)[0].quantity)
                temp += quantity
                Cart.objects.filter(product=product,user=user).update(quantity=temp)
            return JsonResponse({"message" : "Created"}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "KeyError"}, status = 400)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "INVALID_PRODUCT"}, status = 400)

        except json.JSONDecodeError:
            return JsonResponse({"message" : "JsonError"}, status = 400)