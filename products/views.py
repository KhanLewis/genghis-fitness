from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from .models import Product, Category, ProductRating, Comment
from django.db.models import Avg
from django.urls import reverse
from .forms import CommentForm


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


@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return redirect('products:product_detail', pk=product_id)
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'product': product, 'form': form})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('products:product_detail', pk=comment.product.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'comment': comment, 'form': form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == 'POST':
        product_id = comment.product.id
        comment.delete()
        return redirect('products:product_detail', pk=product_id)

    return render(request, 'delete_comment.html', {'comment': comment})
