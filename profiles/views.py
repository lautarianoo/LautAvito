from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from cities.models import City
from .forms import LoginForm, RegisterForm
from django.views import View
from advertisements.mixins import CartMixin
from .models import UserAvito
from advertisements.models import Advertise

class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'profiles/login.html', {'form': form, 'cart': self.cart})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('advertise_list'))
        return render(request, 'profiles/login.html', {'form': form, 'cart': self.cart})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('advertise_list'))

class RegisterView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        cities = City.objects.all()
        city = City.objects.get(title='Москва')
        return render(request, 'profiles/register.html', {'form': form, 'cart': self.cart, 'cities': cities, 'city': city})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'profiles/register.html', {'form': form, 'cart': self.cart})

class ProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        advertises = Advertise.objects.filter(seller=request.user)
        return render(request, 'profiles/profile.html', {'advertises': advertises})

