from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AdvertisementsCategoryList.as_view(), name='advertise_list'),
    path('<slug:slug>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('<slug:category>/<int:pk>/', views.AdvertiseDetail.as_view(), name='advertise_detail'),
    path('cart/', views.CartView.as_view(), name='cart')
]
