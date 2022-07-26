import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Product
from carts.models    import Cart
from core.utils      import LoginConfirm

class CartView(View):
    """
    목적: 장바구니 테이블에 유저와 제품 정보 저장(생성)

    1. Method : POST
    2. 저장하기 위해 필요한 정보
        - 유저 정보 -> 토큰
        - 제품 정보 -> body
        - 수량 -> body
    3. 특수 조건
        - 유저 정보가 디비에 존재 -> 데코레이터
        - 제품이 존제해야 된다. -> 예외조건 
        - 이미 담은 제품일 경우 -> 수량만 증가
        - 수량이 0이하 일 때
        - 제고 관리를 하고 있으면, 제고 < 수량 -> 예외 처리
    """
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

            if not Cart.objects.filter(product=product,user=user).exists():
                Cart.objects.create(
                    user     = user,
                    product  = product,
                    quantity = quantity
                )
            else:
                cart = Cart.objects.get(product=product,user=user)
                cart.quantity += quantity
                cart.save()


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