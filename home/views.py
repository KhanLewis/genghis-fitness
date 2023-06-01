from django.shortcuts import render

# Create your views here.


def index(request):
    """ a view to retyrn the index page """

    return render(request, 'home/index.html')
