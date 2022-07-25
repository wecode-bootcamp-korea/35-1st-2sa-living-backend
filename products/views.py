from django.http  import JsonResponse
from django.views import View

from .models import Product


class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product          = Product.objects.get(id=product_id)
            related_products = Product.objects.filter(furniture_id=product.furniture_id)

            description = [{
                    'english_name'         : product.furniture.english_name + '_' + product.color.english_name,
                    'korean_name'          : product.furniture.korean_name + '_' + product.color.korean_name,
                    'main_image'           : product.main_image_url,
                    'detail_image'         : [image.image_url for image in product.detail_image.all()],
                    'related_products_list': [{
                        'id'   : related_product.id,
                        'color': related_product.color.english_name,
                        'price': related_product.price
                    } for related_product in related_products]
                }]
            return JsonResponse({'description': description}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PRODUCT_ID'}, status=400)
