import json

from django.http import JsonResponse
from django.views import View

from .models import Category, Furniture, SubCategory, Product


class ListView(View):

    '''
    페이지 상단의 (main) category를 클릭하면 
    (main) category 전체와 선택된 (main) category의 sub categoies list를 보여주는 동시에
    해당 (main) category에 속하는 모든 제품의 리스트(이미지, 브랜드, 제품명, 가격 포함)를 보여준다.
    여기에서, sub category(또는 (main) category)를 클릭하면 해당 sub category(또는 (main) category)에 속하는 제품들의 리스트만를 반환한다.

    목적: 사용자가 (main) categories 중 하나를 선택했을 때는 해당하는 sub categories 리스트와 (main) category에 속하는 제품 리스트를 반환하고
        sub categories 중 하나를 선택했을 때는 그 sub category에 속하는 제품 리스트를 반환한다.

    1. client가 보내온 데이터에서 요청하는 category를 받아온다.
    2. 요청받은 category가 (main)인지 sub인지 확인 후 
    3-1. 요청받은 (main) category에 속하는 sub categories를 DB에서 찾는다.
            요청받은 (main) category에 속해있는 제품 전부를 DB에서 찾는다.
            찾은 데이터를 리스트로 만들어서 json파일로 변환하여 반환한다.
    3-2. 요청받은 sub category에 속하는 제품들을 DB에서 찾는다.
            찾은 데이터를 리스트로 반환한다.
    '''

    def get(self, request):
        try:
            data = json.loads(request.body)
            selected_category = data['category']
            '''
            product_list = [{
                'id'         : 5,
                'image'      : 'https://www.abcd',
                'brandName'  : 'HAY',
                'productName': '팔리사이드 쉐이즈 롱_올리브',
                'price'      : 100000
            }]
            '''

            main_categories = Category.objects.all()
            # QuerySet: [ <'id':1, 'name':'소파'>,
            #             <'id':2, 'name':'체어'>,
            #             ... ]
            sub_categories = SubCategory.objects.all()
            # QuerySet: [ <'id':1, 'name':'라운지 체어'>,
            #             <'id':2, 'name':'바 체어'>,
            #             <'id':3, 'name':'키즈 체어'>,
            #             ... ]
            if selected_category in [category.name for category in main_categories]:
                subs = SubCategory.objects.filter(
                    category__name=selected_category)
                sub_list = []
                for sub in subs:
                    sub_list.append(sub.name)
                products = Product.objects.filter(
                    sub_category__category__name=selected_category)

                product_list = []
                for product in products:
                    product_list.append({
                        'id'         : product.id,
                        'image'      : product.thumbnail_image_url,
                        'brandName'  : product.furniture.brand.name,
                        'productName': product.furniture.name + '_' + product.color.name, # 가능? 오 된다
                        'price'      : product.price
                    })
                return JsonResponse({'message': 'SUCCESS', 'sub_list': sub_list, 'product_list': product_list}, status=200)
            elif selected_category in [category.name for category in sub_categories]:
                products = Product.objects.filter(
                    sub_category__name=selected_category)
                product_list = []
                for product in products:
                    product_list.append({
                        'id'         : product.id,
                        'image'      : product.thumbnail_image_url,
                        'brandName'  : product.furniture.brand.name,
                        'productName': product.furniture.name + '_' + product.color.name,
                        'price'      : product.price
                    })
                return JsonResponse({'message': 'SUCCESS', 'product_list': product_list}, status=200)
            else:
                return JsonResponse({'message': 'INVALID_CATEGORY'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSON_ERROR'}, status=400)


class DetailView(View):
    '''
    목적: 사용자가 선택한 제품(product)의 상세정보를 보내준다.
    1. client가 보내온 데이터에서 제품아이디를 받아온다.
    2. 요청받은 product_id에 해당하는 상제 정보를 DB에서 찾는다.
    3. 찾은 데이터를 반환한다.
    '''

    def get(self, request):
        try:
            data       = json.loads(request.body)

            product_id = data['product_id']
            product    = Product.objects.get(id = product_id)

            description = [
                {
                    "english_name": product.furniture.engilsh_name + '_' + product.color.english_name ,
                    'name'        : product.furniture.korean_name + '_' + product.color.korean_name ,
                    'main_image'  : product.main_image_url,
                    'detail_image': product.detail_image.image_url,
                }]

            related_products = Product.objects.filter(Furniture_id = product.furniture_id)

            related_product_list = []
            for related_product in related_products:
                related_product_list.append({
                    'color': related_product.color.korean_name,
                    'price': related_product.price
                })

            return JsonResponse({'description': description, 'related_products': related_product_list}, status=200)

            '''
            'description' : [
                {
                    "english_name": 'Puff Puff Sofa' + '_' + 'Red',
                    'name'        : '퍼프 퍼프 소파' + '_' + '레드',
                    'main_image'  : 'https://aaaaaa',
                    'detail_image': 'https://bbbbb',
                }],
            'related_products' : [
                {
                    'color' : '레드',
                    'price' : 1000000
                },
                {
                    'color' : '화이트',
                    'price' : 1100000
                },
                {
                    'color' : '블랙',
                    'price' : 1500000
                }
            ]
            '''

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSON_ERROR'}, status=400)

