from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AdvertisementsCategoryList.as_view(), name='advertise_list'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-card/<int:pk>/', views.AddtoCartView.as_view(), name='add-to-card'),
    path('<slug:slug>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('<slug:category>/<int:pk>/', views.AdvertiseDetail.as_view(), name='advertise_detail'),
]
