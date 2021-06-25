from django.db import models
from advertisements.models import Advertise
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.contrib.auth.models import AbstractUser


class UserAvito(AbstractUser):

    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100)
    phone = models.CharField(max_length=30, verbose_name='Номер телефона')
    advertises = models.ManyToManyField(Advertise, verbose_name='Объявления', related_name='user')
    email = models.EmailField(verbose_name='Email')
    avatar = models.ImageField(verbose_name='Аватарка', blank=True, null=True)
    company = models.BooleanField(verbose_name='Компания или нет', default=False)

    def __str__(self):
        return f"{self.first_name} | {self.last_name}"

    def save(self, *args, **kwargs):
#
        image = self.avatar
        img = Image.open(image)
        new_img = img.convert('RGB')
        resized_new_img = new_img.resize((400, 300), Image.ANTIALIAS)
        filestream = BytesIO()
        resized_new_img.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image.name.split('.'))
        self.image = InMemoryUploadedFile(
            filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
        )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователя'
