from django.db import models

class User(models.Model):
    email			= models.CharField(max_length=100, unique=True)
    password		= models.CharField(max_length=200)
    first_name		= models.CharField(max_length=50)
    last_name		= models.CharField(max_length=50)
    phone_number	= models.CharField(max_length=100)
    birthdate		= models.DateField()
    created_at		= models.DateTimeField(auto_now_add=True)
    updated_at		= models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Like(models.Model):
    user			= models.ForeignKey('User', on_delete=models.CASCADE)
    product			= models.ForeignKey('products.Product', on_delete=models.CASCADE)
    created_at		= models.DateTimeField(auto_now_add=True)
    updated_at		= models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'likes'