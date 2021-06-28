from django import forms
from .models import Advertise

class AdvertiseForm(forms.ModelForm):

    class Meta:
        model = Advertise
        fields = (
            'category', 'title', 'status', 'city', 'district', 'street', 'image', 'price', 'description'
        )

