from django.shortcuts import render, get_object_or_404
from .models import *

def index(request):
    post = Post.objects.order_by('-created_at')
    context = {'post_list': post}
    return render(request, 'blog/list.html', context)


def get_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post':post}
    return render(request, 'blog/detail.html', {'post':post})