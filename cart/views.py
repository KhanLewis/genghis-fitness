from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, CartItem, Product, Order
from django.contrib import messages
from django.http import JsonResponse


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
            message = 'Item quantity updated in the cart.'
        else:
            message = 'Item added to the cart.'

        cart_items = CartItem.objects.filter(cart=cart)

        data = {
            'message': message,
            'cart_count': cart_items.count()
        }

        return JsonResponse(data)


class RemoveFromCartView(View):
    def post(self, request, cart_item_id):
        cart_item = CartItem.objects.get(id=cart_item_id)
        remove_quantity = request.POST.get('remove_quantity')  # Check if remove_quantity parameter is present

        if remove_quantity:
            quantity = int(remove_quantity)
            if cart_item.quantity <= quantity:
                # If the quantity to be removed is greater than or equal to the current quantity, remove the item
                cart_item.delete()
            else:
                # If the quantity to be removed is less than the current quantity, update the quantity
                cart_item.quantity -= quantity
                cart_item.save()
        else:
            # If remove_quantity parameter is not present, remove the entire item
            cart_item.delete()

        return redirect('cart:cart_detail')



class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)

        cart_items = CartItem.objects.filter(cart=cart)

        for item in cart_items:
            item.total = item.product.price * item.quantity

        cart_total = sum(item.total for item in cart_items)

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'cart_total': cart_total
        }

        return render(request, 'cart/cart_detail.html', context)


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        total_amount = cart.calculate_total()

        order = Order.objects.create(
            user=request.user,
            order_number='ODR123',
            total_amount=total_amount,
            cart=cart
        )

        cart_items.delete()

        messages.success(request, 'Your order has been placed successfully.')

        return redirect('cart:cart_detail')