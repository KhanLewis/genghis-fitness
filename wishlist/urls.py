from django.urls import path
from .views import WishlistView, AddToWishlistView, RemoveFromWishlistView

app_name = 'wishlist'

urlpatterns = [
    path('', WishlistView.as_view(), name='wishlist'),
    path('add/<int:product_id>/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('remove/<int:item_id>/', RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
]
