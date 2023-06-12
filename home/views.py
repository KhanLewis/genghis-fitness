from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.template import RequestContext


class HomeView(TemplateView):
    template_name = 'home/index.html'


class ContactView(TemplateView):
    template_name = 'contact/contact.html'


class PageNotFoundView(View):
    def get(self, request, *args, **kwargs):
        return render(request, '404.html', status=404)
