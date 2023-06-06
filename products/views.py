from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
# Create your views here.


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
        context['average_rating'] = self.object.get_average_rating()
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        rating_value = request.POST.get('rating')

        if rating_value:
            rating = Rating.objects.create(
                product=product,
                user=request.user,
                value=rating_value
            )
            # Redirect to the same product detail page after rating submission
            return HttpResponseRedirect(reverse('products:product_detail', args=(product.id,)))

        return super().get(request, *args, **kwargs)
