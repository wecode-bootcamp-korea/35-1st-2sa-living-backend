import json

from django.http  import JsonResponse
from django.views import View

from .models import Category, Furniture, ProductImage, SubCategory, Product, Brand, Color 


class ProductListView(View):
    def get(self, request):
        category_id     = request.GET.get('category_id', None)
        sub_category_id = request.GET.get('sub_category_id', None)

        products = Product.objects.filter(sub_category_id = sub_category_id) or Product.objects.filter(sub_category__category_id = category_id) 
        product_list = []
        for product in products:
            product_list.append({
                'id'         : product.id,
                'image'      : product.thumbnail_image_url,
                'brandName'  : product.furniture.brand.name,
                'productName': product.furniture.korean_name + '_' + product.color.korean_name,
                'price'      : product.price
            })
        if product_list:
            return JsonResponse({'message': 'SUCCESS', 'product_list': product_list}, status=200)
        else:
            return JsonResponse({'message': 'INVALID_CATEGORY'}, status=400)

