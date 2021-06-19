from django.shortcuts import render
from .models import *
from django.views import View


class AdvertisementsCategoryList(View):
    #Список объявлений

    def get(self, request, *args, **kwargs):
        advertises_list = [advertise for advertise in Advertise.objects.all() if advertise.moderated]
        category = Category.objects.all()
        return render(request, 'base.html', {'advertises': advertises_list, 'categories': category})

class CategoryDetail(View):
    #Детализация категории

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs.get('slug'))
        advertises = Advertise.objects.filter(category=category)
        return render(request, 'advertisements/category_detail.html', {'category': category, 'advertises': advertises})

class AdvertiseDetail(View):
    #Детализация объявлений

    def get(self, request, *args, **kwargs):
        advertise = Advertise.objects.get(id=kwargs.get('pk'))
        return render(request, 'advertisements/advertise_detail.html', {'advertise': advertise})
