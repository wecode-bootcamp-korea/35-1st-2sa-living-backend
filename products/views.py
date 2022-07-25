import json

from django.http  import JsonResponse
from django.views import View
from django.core.paginator import Paginator

from .models import Category, SubCategory, Product


class ProductListView(View):
    def get(self, request):
        category_id     = request.GET.get('category_id', None)
        sub_category_id = request.GET.get('sub_category_id', None)
        page_number     = request.GET.get('page', None)

        if int(category_id) in [c.id for c in Category.objects.all()] and int(sub_category_id) in [c.id for c in SubCategory.objects.all()]:
            products = Product.objects.filter(sub_category_id = sub_category_id) or Product.objects.filter(sub_category__category_id = category_id) 
            product_list = [{
                'id'         : product.id,
                'image'      : product.thumbnail_image_url,
                'brandName'  : product.furniture.brand.name,
                'productName': product.furniture.korean_name + '_' + product.color.korean_name,
                'price'      : product.price
            } for product in products]    

            try: 
                paginator    = Paginator(product_list, 4)
                product_list = paginator.page(page_number).object_list
                page_list    = list(paginator.page_range)
                return JsonResponse({'message': 'SUCCESS', 'product_list': product_list, 'page_list': page_list}, status=200)
            except :
                return JsonResponse({'message': 'INVALID_PAGE'}, status=400)
        else:
            return JsonResponse({'message': 'INVALID_CATEGORY'}, status=400)
    