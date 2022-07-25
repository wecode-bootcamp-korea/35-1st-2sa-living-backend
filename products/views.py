from django.http           import JsonResponse
from django.views          import View
from django.core.paginator import Paginator
from django.db.models      import Q

from .models import Category, SubCategory, Product


class ProductListView(View):
    def get(self, request):
        category_id     = request.GET.get('category_id', None)
        sub_category_id = request.GET.get('sub_category_id', None)
        page_number     = request.GET.get('page', None)


        if int(category_id) in [c.id for c in Category.objects.all()] and int(sub_category_id) in [c.id for c in SubCategory.objects.all()]:
            if SubCategory.objects.get(id=sub_category_id).category == Category.objects.get(id=category_id):
                products = Product.objects.filter(Q(sub_category_id = sub_category_id) & Q(sub_category__category_id = category_id)) 
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
                    return JsonResponse({'message': 'INVALID_PAGE'}, status=404)
            else:
                return JsonResponse({'message': 'DO_NOT_MATCH_CATEGORY'}, status=400)
        else:
            return JsonResponse({'message': 'INVALID_CATEGORY'}, status=404)


class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product          = Product.objects.get(id=product_id)
            related_products = Product.objects.filter(furniture_id=product.furniture_id)

            result = [{
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
            return JsonResponse({'result': result}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PRODUCT_ID'}, status=404)
