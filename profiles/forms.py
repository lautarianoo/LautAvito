from django import forms
from .models import UserAvito
from .models import UserAvito

class LoginForm(forms.Form):

    email = forms.CharField(label='Почтовый ящик', widget=forms.EmailInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not UserAvito.objects.filter(email=email).exists():
            raise forms.ValidationError('Такого пользователя не существует')
        user = UserAvito.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data
