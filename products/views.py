import json

from django.http import JsonResponse
from django.views import View

from .models import Category, Furniture, ProductImage, SubCategory, Product, Brand, Color 


class ListView(View):

    def get(self, request):
        try:
            data = json.loads(request.body)

            selected_category = data['category']

            main_categories = Category.objects.all()
            sub_categories  = SubCategory.objects.all()

            if selected_category in [category.name for category in main_categories]:
                subs = SubCategory.objects.filter(category__name=selected_category)
                
                sub_list = []
                for sub in subs:
                    sub_list.append(sub.name)
                products = Product.objects.filter(sub_category__category__name=selected_category)

                product_list = []
                for product in products:
                    product_list.append({
                        'id'         : product.id,
                        'image'      : product.thumbnail_image_url,
                        'brandName'  : product.furniture.brand.name,
                        'productName': product.furniture.name + '_' + product.color.name,
                        'price'      : product.price
                    })

                return JsonResponse({'message': 'SUCCESS', 'sub_list': sub_list, 'product_list': product_list}, status=200)

            elif selected_category in [category.name for category in sub_categories]:
                products = Product.objects.filter(sub_category__name=selected_category)

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


