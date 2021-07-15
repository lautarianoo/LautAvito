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

class SettingsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['username'].required = False
        self.fields['phone'].required = False

    class Meta:
        model = UserAvito
        fields = ('first_name', 'last_name', 'username', 'phone')
