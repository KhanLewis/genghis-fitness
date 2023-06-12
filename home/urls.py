from django.urls import path
from home.views import HomeView, PageNotFoundView, ContactView

handler404 = PageNotFoundView.as_view()

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
]
