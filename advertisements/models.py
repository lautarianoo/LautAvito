from django.contrib.auth import get_user_model
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

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

class Section(models.Model):
    #Модель подраздела категории

    title = models.CharField(max_length=100, verbose_name='Название секции')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подраздел'
        verbose_name_plural = 'Подразделы'

class Advertise(models.Model):
    #Модель объявления

    STATUS_PRODUCT = (
        ('new', 'Новое'),
        ('bu', 'Б/У'),
    )

    title = models.CharField(verbose_name='Название объявления', max_length=100)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, verbose_name='Подраздел', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(verbose_name='Описание товара', max_length=13000)
    image = models.ImageField(verbose_name='Картинка объявления')
    price  = models.PositiveIntegerField(verbose_name='Цена', default=0, blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertises', verbose_name='Продавец')
    status = models.CharField(verbose_name='Статус товара', choices=STATUS_PRODUCT, max_length=100)
    date_add = models.DateTimeField(verbose_name='Дата создания товара', auto_now_add=True)

    def __str__(self):
        return f"{self.title} | {self.category}"

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
