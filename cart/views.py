from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Cart, CartItem, Product

class AddToCartView(View):
    def post(self, request, product_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart:cart_detail')
