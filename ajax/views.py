from django.http import JsonResponse
from django.shortcuts import render
from cities.models import District

def get_districts(request):
    city = request.GET.get('city', None)
    response = {
        'districts': District.objects.filter(city=city)
    }
    return JsonResponse(response)
