from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from cities.models import City
from .forms import LoginForm, RegisterForm, FeedbackForm, SettingsForm, AcceptEmailForm
from django.views import View
from advertisements.mixins import CartMixin
from .models import UserAvito, Feedback
from advertisements.models import Advertise
from utils.rating import rating
from utils.send_email import send_email

class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'profiles/login.html', {'form': form, 'cart': self.cart})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('advertise_list'))
        return render(request, 'profiles/login.html', {'form': form, 'cart': self.cart})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('advertise_list'))

class RegisterView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        cities = City.objects.all()
        city = City.objects.get(title='Москва')
        return render(request, 'profiles/register.html', {'form': form, 'cart': self.cart, 'cities': cities, 'city': city})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'profiles/register.html', {'form': form, 'cart': self.cart})

class ProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        advertises = Advertise.objects.filter(seller=request.user)
        return render(request, 'profiles/profile.html', {'advertises': advertises, 'user': request.user})

class UserView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        user = UserAvito.objects.get(id=kwargs.get('pk'))
        advertises = Advertise.objects.filter(seller=user)
        feedbacks = Feedback.objects.filter(getter_id=kwargs.get('pk'))
        average = rating(feedbacks)
        return render(request, 'profiles/user_profile.html', {'user': user, 'advertises': advertises, 'cart': self.cart, 'average': average, 'quantity': len(feedbacks)})

class FeedbackCreateView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = FeedbackForm()
        form.advertise = Advertise.objects.filter(seller_id=kwargs.get('pk'))
        return render(request, 'profiles/feedback_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST or None)
        if form.is_valid():
            new_feedback = form.save(commit=False)
            new_feedback.sender = request.user
            new_feedback.getter = UserAvito.objects.get(id=kwargs.get('pk'))
            new_feedback.save()
            if new_feedback:
                request.user.feedbacks.add(new_feedback)
            return redirect('profile_user', pk=kwargs.get('pk'))
        return render(request, 'profiles/feedback_create.html', {'form': form})

class FeedbackView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        feedbacks = Feedback.objects.filter(getter_id=kwargs.get('pk'))
        average = rating(feedbacks)
        return render(request, 'profiles/feedbacks_user.html', {'feedbacks': feedbacks, 'cart': self.cart,
                                                                'user': UserAvito.objects.get(id=kwargs.get('pk')), 'average': average})

class SettingsView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        form = SettingsForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username,
                                     'email': user.email, 'phone': user.phone})
        return render(request, 'profiles/settings.html', {'form': form, 'cart': self.cart})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = SettingsForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.username = data['username']
            user.phone = data['phone']
            user.save()
            return HttpResponseRedirect(reverse('profile'))
        else:
            form = SettingsForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username,
                                     'email': user.email, 'phone': user.phone})
            return render(request, 'profiles/settings.html', {'form': form, 'cart': self.cart})

class AcceptEmail(View):

    def get(self, request, *args, **kwargs):
        form = AcceptEmailForm()
        send_email(request.user.email, form.right_key)
        return render(request, 'profiles/accept_email.html', {'accept_form': form})

    def post(self, request, *args, **kwargs):
        form = AcceptEmailForm(request.POST or None)
        if form.is_valid():
            request.user.status_email = True
            request.user.save()
            return redirect('profile')
        return render(request, 'profiles/accept_email.html', {'accept_form': form})
