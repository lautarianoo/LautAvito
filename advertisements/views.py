from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView

from .models import *
from django.views import View
from .mixins import CartMixin


class AdvertisementsCategoryList(CartMixin, View):
    #Список объявлений

    def get(self, request, *args, **kwargs):
        advertises_list = [advertise for advertise in Advertise.objects.all() if advertise.moderated]
        category = Category.objects.all()
        city = City.objects.all()
        return render(request, 'base.html', {'advertises': advertises_list, 'categories': category, 'cart': self.cart, 'cities': city})


class CategoryDetail(CartMixin, View):
    #Детализация категории

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs.get('slug'))
        advertises = Advertise.objects.filter(category=category)
        return render(request, 'advertisements/category_detail.html', {'category': category, 'advertises': advertises, 'cart': self.cart})

class AdvertiseDetail(CartMixin, View):
    #Детализация объявлений

    def get(self, request, *args, **kwargs):
        advertise = Advertise.objects.get(id=kwargs.get('pk'))
        return render(request, 'advertisements/advertise_detail.html', {'advertise': advertise, 'cart': self.cart})

class CartView(CartMixin, View):
    #Корзина

    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        return render(request, 'advertisements/cart.html', {'categories': category, 'cart': self.cart})

class AddtoCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        advertise = Advertise.objects.get(id=kwargs.get('pk'))
        if advertise:
            self.cart.advertisements.add(advertise)
            self.cart.quality += 1
        messages.add_message(request, messages.INFO, 'Добавлено в избранные')
        return HttpResponseRedirect(reverse('cart'))

class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        advertise = Advertise.objects.get(id=kwargs.get('pk'))
        self.cart.advertisements.remove(advertise)
        messages.add_message(request, messages.INFO, 'Товар успешно удален')
        return HttpResponseRedirect(reverse('cart'))

class TitleSearching(CartMixin, View):

    def get(self, request, *args, **kwargs):
        advertises = Advertise.objects.filter(
            title__icontains=request.GET.get('title'))
        categories = Category.objects.all()
        return render(request, 'base.html', {'advertises': advertises, 'categories': categories, 'cart': self.cart})
