from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    category_view,
    add_comment,
    edit_comment,
    delete_comment,
)

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path(
        'product/<int:pk>/',
        ProductDetailView.as_view(),
        name='product_detail'),
    path(
        'category/<slug:slug>/',
        category_view, name='category_view'),
    path(
        'product/<int:product_id>/add_comment/',
        add_comment, name='add_comment'),
    path(
        'comment/<int:comment_id>/edit/',
        edit_comment, name='edit_comment'),
    path(
        'comment/<int:comment_id>/delete/',
        delete_comment, name='delete_comment'),
]
