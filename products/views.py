from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import DetailView, ListView
from .models import Product, Category, ProductRating
from django.db.models import Avg
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        average_rating = product.product_ratings.aggregate(average_rating=Avg('rating')).get('average_rating', 0)
        context['average_rating'] = average_rating
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = self.get_object()
            rating_value = request.POST.get('rating')

            # Check if the user has already rated this product
            existing_rating = ProductRating.objects.filter(product=product, user=request.user).first()
            if existing_rating:
                return HttpResponseRedirect(reverse('products:product_detail', args=(product.pk,)))

            if rating_value:
                rating = ProductRating.objects.create(
                    product=product,
                    user=request.user,
                    rating=rating_value
                )
                return HttpResponseRedirect(reverse('products:product_detail', args=(product.pk,)))

        return super().post(request, *args, **kwargs)
