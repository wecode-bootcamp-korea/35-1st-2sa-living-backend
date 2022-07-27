from django.http       import JsonResponse
from django.views      import View
from django.db.models  import Q

from products.models import Category, SubCategory, Product

class ProductListView(View):
    def get(self, request):
        try:
            DEFAULT_LIMIT = 4
            DEFAULT_OFFSET = 0

            category_id     = request.GET.get('category_id', None)
            sub_category_id = request.GET.get('sub_category_id', None)
            limit           = int(request.GET.get('limit', DEFAULT_LIMIT))
            offset          = int(request.GET.get('offset', DEFAULT_OFFSET))
            sort_type       = int(request.GET.get('sort_type', 1))  
            
            sub_category_q = Q()

            product_q = Q()

            if category_id:
                category        = Category.objects.get(id = category_id)
                sub_category_q &= Q(category=category)
                product_q      &= Q(sub_category__category = category)

            if sub_category_id:
                sub_category    = SubCategory.objects.get(id = sub_category_id)
                sub_category_q &= Q(category=sub_category.category)
                product_q      &= Q(sub_category = sub_category)
            
            count = len(Product.objects.filter(product_q))

            sub_category_list = [ sub_category.name for sub_category in SubCategory.objects.filter(sub_category_q) ]

            sort_set = { 
                1: 'id',
                2: 'furniture__updated_at',
                3: '-price',
                4: 'price',
            }

            sort_field = sort_set.get(sort_type, 'id')       

            products = Product.objects.filter(product_q).order_by(sort_field)[offset:offset+limit]
            
            product_list = [{
                'id'         : product.id,
                'image'      : product.thumbnail_image_url,
                'brandName'  : product.furniture.brand.name,  
                'productName': product.furniture.korean_name + '_' + product.color.korean_name,
                'price'      : product.price
            } for product in products]                

            return JsonResponse({'message': 'SUCCESS', 'count': count, 'sub_category_list': sub_category_list, 'product_list': product_list}, status=200)
        except Category.DoesNotExist:
            return JsonResponse({'message': 'INVALID_CATEGORY'}, status=404)
        except SubCategory.DoesNotExist:   
            return JsonResponse({'message': 'INVALID_SUBCATEGORY'}, status=404)                 

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product          = Product.objects.get(id=product_id)
            related_products = Product.objects.filter(furniture_id=product.furniture_id)

            result = {
                    'english_name'         : product.furniture.english_name + '_' + product.color.english_name,
                    'korean_name'          : product.furniture.korean_name + '_' + product.color.korean_name,
                    'main_image'           : product.main_image_url,
                    'detail_image'         : [image.image_url for image in product.detail_image.all()],
                    'related_products_list': [{
                        'id'   : related_product.id,
                        'color': related_product.color.english_name,
                        'price': related_product.price
                    } for related_product in related_products]
                }
            return JsonResponse({'result': result}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PRODUCT_ID'}, status=404)
