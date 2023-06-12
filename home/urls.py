from django.urls import path
from home.views import HomeView, PageNotFoundView

handler404 = PageNotFoundView.as_view()

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
