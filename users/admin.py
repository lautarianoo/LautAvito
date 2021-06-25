from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import  *

#class UserNetAdmin(UserAdmin):
#    list_display = ('username', 'email', 'phone', 'first_name', 'last_name', 'is_staff')
#    fieldsets = (
#        (None, {'fields': ('username', 'password')}),
#        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
#        (('Permissions'), {
#            'fields': ('is_active', 'is_staff', 'is_superuser'),
#        }),
#        (('Doc info'), {'fields': ('phone', 'avatar', 'advertises', 'email')})),

admin.site.register(UserAvito)
