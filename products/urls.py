from django.urls import path
from .views import ProductListView, ProductDetailView, category_view

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', category_view, name='category_view'),
]
