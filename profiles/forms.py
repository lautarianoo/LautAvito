from django import forms
from .models import UserAvito
from .models import UserAvito, Feedback

class LoginForm(forms.Form):

    email = forms.CharField(label='Почта', widget=forms.EmailInput())
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

class RegisterForm(forms.ModelForm):

    #email = forms.CharField(label='Почтовый ящик', widget=forms.EmailInput())
    #phone = forms.CharField(label='Номер телефона')
    #username = forms.CharField(label='Прозвище')
    #first_name = forms.CharField(label='Имя')
    #last_name = forms.CharField(label='Фамилия')
    #city = forms.CharField(label='Город')
    #avatar = forms.ImageField(label='Аватарка', widget=forms.FileInput(), required=False)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = UserAvito
        fields = ('email', 'phone', 'username', 'first_name', 'last_name', 'city', 'avatar')

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ('advertise', 'text', 'mark')
