from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Timestampable(models.Model):
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата редактирования', auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'customer'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    email = models.EmailField('Email', null=False, blank=False, unique=True)
    first_name = models.CharField('Имя', max_length=255, blank=True)
    last_name = models.CharField('Фамилия', max_length=255, blank=True)
    is_active = models.BooleanField('Признак активности', default=False)

    USERNAME_FIELD = 'email'

    objects = BaseUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ('last_name', 'first_name')

    def __str__(self):
        return f'{self.last_name} {self.first_name} '


class Album(models.Model):
    created_by = models.ForeignKey('User', on_delete=models.CASCADE)
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)


class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ['album', 'order']
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.title)


class Category(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255, null=True, blank=True, unique=True)
    parent = models.ForeignKey('self', verbose_name='Parent',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               related_name='children')

    def __str__(self):
        return self.name

    def get_all_children(self, container=None, include_self=False):
        if container is None:
            if include_self:
                container = [self]
            else:
                container = []
        result = container
        for child in self.children.all():
            result.append(child)
            if child.children.count() > 0:
                child.get_all_children(result)
        return result


class Product(models.Model):
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return self.brand.title + ' ' + str(self.price)


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

    def __str__(self):
        return self.title


class BrandModel(models.Model):
    title = models.CharField(max_length=32)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    sale_date = models.DateTimeField()