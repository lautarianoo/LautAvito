from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('user/<int:pk>/', views.UserView.as_view(), name='profile_user'),
    path('user/<int:pk>/feedback-add/', views.FeedbackCreateView.as_view(), name='feedback-add'),
    path('user/<int:pk>/feedbacks/', views.FeedbackView.as_view(), name='feedbacks_user')
]
