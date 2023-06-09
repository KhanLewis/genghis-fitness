from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Product, Category, ProductRating
from django.db.models import Avg
from django.urls import reverse


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = Product.objects.filter(category=category)
        else:
            queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'products/products.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        average_rating = product.product_ratings.aggregate(average_rating=Avg('rating')).get('average_rating')
        context['average_rating'] = round(average_rating, 1) if average_rating is not None else 0
        context['has_rated'] = False

        if self.request.user.is_authenticated:
            existing_rating = ProductRating.objects.filter(product=product, user=self.request.user).first()
            if existing_rating:
                context['has_rated'] = True

        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = self.get_object()
            rating_value = request.POST.get('rating')

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
