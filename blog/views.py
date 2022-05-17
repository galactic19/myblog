from django.shortcuts import render
from .models import *

def index(request):
    post = Post.objects.order_by('-created_at')
    
    context = {'post_list': post}
    return render(request, 'blog/list.html', context)