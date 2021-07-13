from django import forms
from .models import Advertise
from cities.models import District
from advertisements.mixins import DistrictMixin

class AdvertiseForm(forms.ModelForm):

    image_main = forms.ImageField(label='Главное изображение')
    image_2 = forms.ImageField(required=False, label='Изображение')
    image_3 = forms.ImageField(required=False, label='Изображение')
    image_4 = forms.ImageField(required=False, label='Изображение')
    image_5 = forms.ImageField(required=False, label='Изображение')


    class Meta:
        model = Advertise
        fields = (
            'category', 'title', 'status', 'city', 'district', 'street', 'price', 'description'
        )

