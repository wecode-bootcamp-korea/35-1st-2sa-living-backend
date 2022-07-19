from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'


class SubCategory(models.Model):
    name     = models.CharField(max_length=45)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'


class Brand(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'brands'


class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'


class Furniture(models.Model):
    name       = models.CharField(max_length=45)
    brand      = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'furnitures'


class Product(models.Model):
    thumnail_image_url = models.CharField(max_length=200)
    main_image_url     = models.CharField(max_length=200)
    price              = models.IntegerField()
    is_new             = models.BooleanField()
    sub_category       = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    cololr             = models.ForeignKey(Color, on_delete=models.CASCADE)
    Furniture          = models.ForeignKey(Furniture, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'


class ProductImage:
    image_url = models.CharField(max_length=45)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'