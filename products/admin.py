from django.contrib import admin
from .models import Product, Category, ProductRating, Comment
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductRating)
admin.site.register(Comment)
