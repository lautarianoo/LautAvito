from django import forms
from .models import Advertise
from cities.models import District
from advertisements.mixins import DistrictMixin

class AdvertiseForm(forms.ModelForm):

    class Meta:
        model = Advertise
        fields = (
            'category', 'title', 'status', 'city', 'district', 'street', 'image', 'price', 'description'
        )

