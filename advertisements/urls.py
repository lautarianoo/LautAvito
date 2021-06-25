from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AdvertisementsCategoryList.as_view(), name='advertise_list'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-card/<int:pk>/', views.AddtoCartView.as_view(), name='add-to-card'),
    path('delete-from-card/<int:pk>/', views.DeleteFromCartView.as_view(), name='delete-from-card'),
    path('search-advertise/', views.TitleSearching.as_view(), name='search_adv'),
    path('change-city/<int:pk>/', views.ChangeCity.as_view(), name='change_city'),
    path('<slug:slug>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('<slug:category>/<int:pk>/', views.AdvertiseDetail.as_view(), name='advertise_detail'),
]
