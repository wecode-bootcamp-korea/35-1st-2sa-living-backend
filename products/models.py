from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'
        
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name     = models.CharField(max_length=45)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.name

class Color(models.Model):
    name         = models.CharField(max_length=45)
    english_name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

    def __str__(self):
        return self.name

class Furniture(models.Model):
    name         = models.CharField(max_length=45)
    english_name = models.CharField(max_length=45)
    brand        = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'furnitures'

    def __str__(self):
        return self.name

class Product(models.Model):
    thumbnail_image_url = models.CharField(max_length=200)
    main_image_url      = models.CharField(max_length=200)
    price               = models.DecimalField(max_digits=11, decimal_places=2)
    is_new              = models.BooleanField()
    sub_category        = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    color               = models.ForeignKey(Color, on_delete=models.CASCADE)
    furniture           = models.ForeignKey(Furniture, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

class ProductImage:
    image_url = models.CharField(max_length=45)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'