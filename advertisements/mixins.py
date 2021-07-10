from django.views import View
from .models import Cart
from cities.models import District

class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(owner=request.user).first()
            if not cart:
                cart = Cart.objects.create(owner=request.user)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)

class DistrictMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            districts = District.objects.filter(city=request.user.city)
            self.districts = districts
        return super().dispatch(request, *args, **kwargs)
