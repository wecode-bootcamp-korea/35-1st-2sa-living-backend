# Generated by Django 4.0.6 on 2022-07-20 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='english_name',
            field=models.CharField(default='', max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='furniture',
            name='english_name',
            field=models.CharField(default='', max_length=45),
            preserve_default=False,
        ),
    ]