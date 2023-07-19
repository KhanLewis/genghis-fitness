from django.views.generic import ListView
from .models import Blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
