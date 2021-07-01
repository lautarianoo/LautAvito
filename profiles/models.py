from django.db import models
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.contrib.auth.models import AbstractUser
from cities.models import City

class Feedback(models.Model):

    STATUS_FEEDBACK = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    sender = models.ForeignKey('UserAvito', verbose_name='Отправитель', on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=1500)
    advertise = models.ForeignKey('advertisements.Advertise', verbose_name='Объявление', related_name='feedbacks', on_delete=models.CASCADE)
    getter = models.ForeignKey('UserAvito', verbose_name='Получатель', on_delete=models.SET_NULL, null=True, related_name='feedbacks_getter')
    mark = models.CharField(choices=STATUS_FEEDBACK, verbose_name='Оценка', max_length=400)

    def __str__(self):
        return f"{self.sender.username} | {self.advertise.title}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class UserAvito(AbstractUser):

    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100)
    phone = models.CharField(max_length=30, verbose_name='Номер телефона')
    feedbacks = models.ManyToManyField(Feedback, verbose_name='Отзывы', related_name='user')
    advertises = models.ManyToManyField('advertisements.Advertise', verbose_name='Объявления', related_name='user')
    email = models.EmailField(verbose_name='Email')
    avatar = models.ImageField(verbose_name='Аватарка', blank=True, null=True)
    company = models.BooleanField(verbose_name='Компания или нет', default=False)
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.SET_NULL, null=True, related_name='user_related')

    def __str__(self):
        return f"{self.username} | {self.last_name}"

    def save(self, *args, **kwargs):
#
        if self.avatar:
            image = self.avatar
            img = Image.open(image)
            new_img = img.convert('RGB')
            resized_new_img = new_img.resize((400, 300), Image.ANTIALIAS)
            filestream = BytesIO()
            resized_new_img.save(filestream, 'JPEG', quality=90)
            filestream.seek(0)
            name = '{}.{}'.format(*self.avatar.name.split('.'))
            self.avatar = InMemoryUploadedFile(
                filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователя'

