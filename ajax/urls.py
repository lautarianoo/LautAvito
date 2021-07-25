from django.urls import path
from . import views

urlpatterns = [
    path('get_districts', views.get_districts, name='get_districts')
]
