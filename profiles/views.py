from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from cities.models import City
from .forms import LoginForm
from django.views import View
from advertisements.mixins import CartMixin
from .models import UserAvito

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
