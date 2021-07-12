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
        advertises = Advertise.objects.all()
        if request.user.is_authenticated:
            city_user = City.objects.get(user_related=request.user)
            advertises = Advertise.objects.filter(moderated=True, city=city_user)
            cities = City.objects.all()
            return render(request, 'base.html', {'advertises': advertises, 'categories': category, 'cart': self.cart,
                                                 'cities': cities, 'city_user': city_user})
        return render(request, 'base.html', {'advertises': advertises, 'categories': category})

class CategoryDetail(CartMixin, View):
    #Детализация категории

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs.get('slug'))
        if request.user.is_authenticated:
            city_user = City.objects.get(user_related=request.user)
            advertises = Advertise.objects.filter(category=category, moderated=True, city=city_user)
            cities = City.objects.all()
            return render(request, 'advertisements/category_detail.html',
                          {'category': category, 'advertises': advertises, 'cart': self.cart, 'cities': cities,
                           'city_user': city_user})
        advertises = Advertise.objects.filter(category=category)
        return render(request, 'advertisements/category_detail.html', {'category': category, 'advertises': advertises})

class AdvertiseDetail(CartMixin, View):
    #Детализация объявлений

    def get(self, request, *args, **kwargs):
        advertise = Advertise.objects.get(id=kwargs.get('pk'))
        advertise.viewed += 1
        advertise.save()
        if request.user.is_authenticated:
            cities = City.objects.all()
            city_user = City.objects.get(user_related=request.user)
            return render(request, 'advertisements/advertise_detail.html', {'advertise': advertise, 'cart': self.cart, 'cities': cities, 'city_user': city_user})
        return render(request, 'advertisements/advertise_detail.html', {'advertise': advertise})

class CartView(CartMixin, View):
    #Корзина
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        category = Category.objects.all()
        cities = City.objects.all()
        city_user = City.objects.get(user_related=request.user)
        return render(request, 'advertisements/cart.html', {'categories': category, 'cart': self.cart, 'cities': cities, 'city_user': city_user})

class AddtoCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        advertise = Advertise.objects.get(id=kwargs.get('pk'))
        if advertise:
            self.cart.advertisements.add(advertise)
            self.cart.quality += 1
        messages.add_message(request, messages.INFO, 'Добавлено в избранные')
        return HttpResponseRedirect(reverse('cart'))

class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        advertise = Advertise.objects.get(id=kwargs.get('pk'))
        self.cart.advertisements.remove(advertise)
        messages.add_message(request, messages.INFO, 'Товар успешно удален')
        return HttpResponseRedirect(reverse('cart'))

class DeleteFromBase(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
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
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        user = request.user
        city = City.objects.get(id=kwargs.get('pk'))
        user.city = city
        user.save()
        return HttpResponseRedirect(reverse('advertise_list'))

class AdvertiseAddView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        form = AdvertiseForm(initial={'city': request.user.city})
        categories = Category.objects.all()
        cities = City.objects.all()
        city_user = City.objects.get(user_related=request.user)
        return render(request, 'advertisements/advertise_form.html',
                      {'form': form, 'categories': categories, 'cart': self.cart, 'cities': cities,
                       'city_user': city_user})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        form = AdvertiseForm(request.POST or None)
        if form.is_valid():
            new_ad = form.save(commit=False)
            new_ad.seller = request.user
            photos = PhotosAdvertise.objects.create(title=request.user.username, image_main=new_ad.image_main,
                                           image_2=new_ad.image_2, image_3=new_ad.image_3,
                                           image_4=new_ad.image_4, image_5=new_ad.image_5)
            new_ad.images = photos
            new_ad.save()
            return HttpResponseRedirect(reverse('advertise_list'))
        return render(request, 'advertisements/advertise_form.html',
                      {'form': form, 'cart': self.cart})

class MyAdvertiseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        advertises = Advertise.objects.filter(seller=request.user)
        cities = City.objects.all()
        city_user = City.objects.get(user_related=request.user)
        return render(request, 'advertisements/my_advertise.html',
                      {'advertises': advertises, 'cart': self.cart, 'cities': cities,
                       'city_user': city_user})


