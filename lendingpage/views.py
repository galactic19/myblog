from django.http import HttpResponse
from django.shortcuts import render, HttpResponse

from django.views.generic import ListView, DetailView
from .models import *
from blog.models import Post


def mainList(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(request, 'lendingpage/lendingpage_list.html', {'recent_posts':recent_posts})
    
    