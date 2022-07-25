import csv
import os
from unicodedata import category
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_2sa_living.settings")
django.setup()

from products.models import *



# with open('products.txt','w') as file:
#     file.write('HELLO WORLD!')

with open('products.txt', 'r') as file:
    # line = None
    # while line != '':
    #     line = file.readline()
    #     print(line.strip('\n'))

    # for line in file:
    #     print(line.strip('\n'))

    data_reader = csv.reader(file, delimiter='\t')
    next(data_reader, None)
    for row in data_reader:
        # print(row[1])
        categories    = Category.objects.all()
        category_list = [category.name for category in categories]     
        if row[1] not in category_list :
            Category.objects.create( name = row[1] )

        sub_categories    = SubCategory.objects.all()
        sub_category_list = [category.name for category in sub_categories]
        if row[2] not in sub_category_list:
            SubCategory.objects.create( name = row[2], category = Category.objects.get(name =row[1]) )

        brands     = Brand.objects.all()
        brand_list = [brand.name for brand in brands]
        if row[3] not in brand_list:
            Brand.objects.create( name = row[3] )

        furnitures     = Furniture.objects.all()
        furniture_list = [furniture.korean_name for furniture in furnitures]
        if row[4] not in furniture_list:
            Furniture.objects.create( korean_name = row[4], english_name = row[5], brand = Brand.objects.get(name=row[3]))

        colors     = Color.objects.all()
        color_list = [color.korean_name for color in colors]
        if row[6] not in color_list:
            Color.objects.create( korean_name = row[6], english_name = row[7])

        if not Product.objects.filter(furniture__korean_name=row[4], color__korean_name=row[6]):
            Product.objects.create(
                price               = row[8],
                thumbnail_image_url = row[9],
                main_image_url      = row[10],
                is_new              = row[12],
                sub_category        = SubCategory.objects.get(name=row[2]),
                color               = Color.objects.get(korean_name=row[6]),
                furniture           = Furniture.objects.get(korean_name=row[4])
            )  

        if not ProductImage.objects.filter(image_url=row[11]):
            ProductImage.objects.create( 
                image_url = row[11],
                product   = Product.objects.get(furniture__korean_name=row[4], color__korean_name=row[6])
            ) 
        

print("I WANNA GO HOME..")