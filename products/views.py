from django.http           import JsonResponse
from django.views          import View
from django.core.paginator import Paginator
from django.db.models      import Q

from .models import Category, SubCategory, Product


class ProductListView(View):
    """
    목적: 제품의 목록을 반환

    조건(필터)
        - 카테고리 id로 필터
        - 서브카테고리 id로 필터
    조건(정렬)
        - 신상품
        - 추천
        - 가격
        - 판매
    조건(페이지네이션)

    구현 순선
        1. 조건이 하나도 없는 제품 목록을 반환
        2. 필터 조건을 1개씩만 구현
        3. 만족한 조건들을 다 합쳐서 구현
        4. 정렬
        5. 페이지네이션

    """

    """
    1. Request로 받은 값들 검증
    2. 로직
        - filter 조건만 조합
        - 정렬 조건 확인
        - 위에서 만든 조건으로 QuerySet을 가져옵니다. + 페이지네이션
    3. Response
    
    """
    
    def get(self, request):
        #:8000/products?category_id=1&category_id=3
        
        try:
            category_id     = request.GET.get('category_id', None)
            sub_category_id = request.GET.get('sub_category_id', None)
            page_number     = request.GET.get('page', 1)
            sort            = request.GET.get('sort')

            q = Q()
            
            if category_id:
                category = Category.objects.get(id = category_id)
                q &= Q(sub_category__category = category)
            
            if sub_category_id:
                sub_category = SubCategory.objects.get(id = sub_category_id)
                q &= Q(sub_category = sub_category)

            sort_set = {
                "new"   : "created_at",
                "price" : "price"
            }

            sort_field = sort_set.get(sort, "id") 

            products = Product.objects.filter(q).order_by(sort_field)
            
            product_list = [{
                'id'         : product.id,
                'image'      : product.thumbnail_image_url,
                'brandName'  : product.furniture.brand.name,  
                'productName': product.furniture.korean_name + '_' + product.color.korean_name,
                'price'      : product.price
            } for product in products]    
            
            paginator    = Paginator(product_list, 4)
            product_list = paginator.page(page_number).object_list
            page_list    = list(paginator.page_range)

            return JsonResponse({'message': 'SUCCESS', 'product_list': product_list, 'page_list': page_list}, status=200)
        except Category.DoesNotExist:
            return JsonResponse({'message': 'INVALID_CATEGORY'}, status=404)
        except SubCategory.DoesNotExist:   
            return JsonResponse({'message': 'INVALID_SUBCATEGORY'}, status=404)        
        except Paginator.EmptyPage:
            return JsonResponse({'message': 'INVALID_PAGE'}, status=404)        
            

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
