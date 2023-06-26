from django.shortcuts import render, redirect,  get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from products.models import Product
from .models import Wishlist, WishlistItem


class WishlistView(View):
    def get(self, request):
        """A view that renders the wishlist contents page"""
        wishlist = Wishlist.objects.filter(user=request.user).first()
        context = {
            'wishlist': wishlist
        }
        return render(request, 'wishlist/wishlist.html', context)


class AddToWishlistView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        size = request.POST.get('size')  

        wishlist = Wishlist.objects.filter(user=request.user).first()

        if wishlist:
            wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, product=product, size=size).first()
            if wishlist_item:
                messages.info(request, f' {product.name} Size: {size} already exists in your wishlist.')
            else:
                wishlist_item = WishlistItem.objects.create(wishlist=wishlist, product=product, size=size)
                messages.success(request, f'Added size: {size} {product.name} to your wishlist.')
        else:
            wishlist = Wishlist.objects.create(user=request.user)
            WishlistItem.objects.create(wishlist=wishlist, product=product, size=size)
            messages.success(request, f'Added size: {size} {product.name} added to your wishlist.')

        return redirect('wishlist:wishlist')


class RemoveFromWishlistView(View):
    def post(self, request, item_id):
        """Remove an item from the user's wishlist"""
        try:
            wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)

            # Get the product details before deleting the item
            product_name = wishlist_item.product.name
            product_size = wishlist_item.size
            wishlist_item.delete()
            messages.success(request, f'Product "{product_name}" (Size: {product_size}) removed from your wishlist.')

            return HttpResponse(status=200)
        except Exception as e:
            messages.error(request, f'Error removing item: {e}')
            return HttpResponse(status=500)
