from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255, null=True, blank=True, unique=True)
    parent = models.ForeignKey('self', verbose_name='Parent',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               related_name='children')

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    price = models.FloatField()


class Sneaker(Product):
    SUBTYPE_1 = '1'
    SUBTYPE_2 = '2'

    SNEAKER_CHOICES = (
        (SUBTYPE_1, '1'),
        (SUBTYPE_2, '2')
    )
    subtype = models.CharField(choices=SNEAKER_CHOICES, max_length=1)


class Bag(Product):
    pass


class Brand(models.Model):
    title = models.CharField(max_length=32)


class BrandModel(models.Model):
    title = models.CharField(max_length=32)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale_date = models.DateTimeField()