from django.urls import path
from .views import AddToCartView, RemoveFromCartView, CartDetailView

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:cart_item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('', CartDetailView.as_view(), name='cart_detail'),
]
