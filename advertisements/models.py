import sys
from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from cities.models import City, Street, District

User = get_user_model()

class Category(models.Model):
    #Модель категорий

    title = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name  = 'Категория'
        verbose_name_plural = 'Категории'


class Advertise(models.Model):
    #Модель объявления

    STATUS_PRODUCT = (
        ('Новое', 'Новое'),
        ('Б/У', 'Б/У'),
    )

    title = models.CharField(verbose_name='Название объявления', max_length=100)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE, related_name='advertises')
    district = models.ForeignKey(District, verbose_name='Район', on_delete=models.SET_NULL, related_name='advertises',
                                 null=True)
    street = models.ForeignKey(Street, verbose_name='Улица', on_delete=models.SET_NULL,
                               blank=True, null=True)
    description = models.TextField(verbose_name='Описание товара', max_length=13000)
    images = models.ForeignKey('PhotosAdvertise', verbose_name='Изображения товара', on_delete=models.CASCADE)
    price  = models.PositiveIntegerField(verbose_name='Цена', default=0,
                                         blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertises_user', verbose_name='Продавец')
    status = models.CharField(verbose_name='Статус товара', choices=STATUS_PRODUCT, max_length=100)
    viewed = models.IntegerField(default=0)
    date_add = models.DateTimeField(verbose_name='Дата создания товара', auto_now_add=True)
    moderated = models.BooleanField(verbose_name='Просмотрено модератором', default=False)

    def __str__(self):
        return f"{self.title} | {self.category}"

    def get_main_image(self):
        return self.images.image_main

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

class PhotosAdvertise(models.Model):

    title = models.CharField(max_length=150, verbose_name='Название изображения')
    image_main = models.ImageField(verbose_name='Изображение главное')
    image_2 = models.ImageField(verbose_name='Изображение 2', blank=True, null=True)
    image_3 = models.ImageField(verbose_name='Изображение 3', blank=True, null=True)
    image_4 = models.ImageField(verbose_name='Изображение 4', blank=True, null=True)
    image_5 = models.ImageField(verbose_name='Изображение 5', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        images = [self.image_main, self.image_2, self.image_3, self.image_4, self.image_5]

        for i in range(0, len(images)):
            img = Image.open(images[i])
            new_img = img.convert('RGB')
            resized_new_img = new_img.resize((500, 500), Image.ANTIALIAS)
            filestream = BytesIO()
            resized_new_img.save(filestream, 'JPEG', quality=90)
            filestream.seek(0)
            name = '{}.{}'.format(*images[i].name.split('.'))
            images[i] = InMemoryUploadedFile(
                filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
            )
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

class Cart(models.Model):
    #Модель понравившихся товаров(корзина)

    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE, null=True)
    advertisements = models.ManyToManyField(Advertise, verbose_name='Товары', related_name='cart')
    quality = models.PositiveIntegerField(default=0)
    for_anonymous_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
