from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView

from .models import *
from django.views import View
from .mixins import CartMixin
from .forms import AdvertiseForm


class AdvertisementsCategoryList(CartMixin, View):
    #Список объявлений

    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        cities = City.objects.all()
        city_user = City.objects.get(user_related=request.user)
        advertises = Advertise.objects.filter(moderated=True, city=city_user)
        return render(request, 'base.html', {'advertises': advertises, 'categories': category, 'cart': self.cart,
                                             'cities': cities, 'city_user': city_user})


class CategoryDetail(CartMixin, View):
    #Детализация категории

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs.get('slug'))
        city_user = City.objects.get(user_related=request.user)
        advertises = Advertise.objects.filter(category=category, moderated=True, city=city_user)
        cities = City.objects.all()
        return render(request, 'advertisements/category_detail.html', {'category': category, 'advertises': advertises, 'cart': self.cart, 'cities': cities, 'city_user': city_user})

class AdvertiseDetail(CartMixin, View):
    #Детализация объявлений

    def get(self, request, *args, **kwargs):
        advertise = Advertise.objects.get(id=kwargs.get('pk'))
        cities = City.objects.all()
        city_user = City.objects.get(user_related=request.user)
        return render(request, 'advertisements/advertise_detail.html', {'advertise': advertise, 'cart': self.cart, 'cities': cities, 'city_user': city_user})

class CartView(CartMixin, View):
    #Корзина

    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        cities = City.objects.all()
        city_user = City.objects.get(user_related=request.user)
        return render(request, 'advertisements/cart.html', {'categories': category, 'cart': self.cart, 'cities': cities, 'city_user': city_user})

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

class DeleteFromBase(View):

    def get(self, request, *args, **kwargs):
        advertise = Advertise.objects.get(id=kwargs.get('pk'))
        advertise.delete()
        messages.add_message(request, messages.INFO, 'Товар снят с публикации')
        return HttpResponseRedirect(reverse('my_ad'))

class TitleSearching(CartMixin, View):

    def get(self, request, *args, **kwargs):
        advertises = Advertise.objects.filter(
            title__icontains=request.GET.get('title'))
        categories = Category.objects.all()
        cities = City.objects.all()
        city_user = City.objects.get(user_related=request.user)
        return render(request, 'base.html', {'advertises': advertises, 'categories': categories, 'cart': self.cart, 'cities': cities, 'city_user': city_user})

class ChangeCity(CartMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        city = City.objects.get(id=kwargs.get('pk'))
        user.city = city
        user.save()
        return HttpResponseRedirect(reverse('advertise_list'))

class AdvertiseAddView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = AdvertiseForm()
        categories = Category.objects.all()
        cities = City.objects.all()
        city_user = City.objects.get(user_related=request.user)
        return render(request, 'advertisements/advertise_form.html',
                      {'form': form, 'categories': categories, 'cart': self.cart, 'cities': cities,
                       'city_user': city_user})

    def post(self, request, *args, **kwargs):
        form = AdvertiseForm(request.POST or None)
        if form.is_valid():
            new_ad = form.save(commit=False)
            new_ad.seller = request.user
            new_ad.save()
            return HttpResponseRedirect(reverse('advertise_list'))
        return render(request, 'advertisements/advertise_form.html',
                      {'form': form, 'cart': self.cart})


class MyAdvertiseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        advertises = Advertise.objects.filter(seller=request.user)
        cities = City.objects.all()
        city_user = City.objects.get(user_related=request.user)
        return render(request, 'advertisements/my_advertise.html',
                      {'advertises': advertises, 'cart': self.cart, 'cities': cities,
                       'city_user': city_user})


