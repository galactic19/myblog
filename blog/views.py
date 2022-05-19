from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView
from .models import *


class BlogView(ListView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context        


# Class 형 View 를 만들기 위해 FBV 는 주석 처리
# def index(request, category_slug=None):
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         # category = Category.objects.get(slug=category_slug)
#         post = category.post_set.order_by('-created_at')
#     else:
#         category = Category.objects.all()
#         post = Post.objects.all()

#     context = {'post_list': post, 'category':category}
#     return render(request, 'blog/list.html', context)


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context        
    
    
# Class View 사용하기 위한 주석 처리
# def get_detail(request, pk, category_id=None):
#     post = get_object_or_404(Post, pk=pk)
#     context = {'post':post}
#     return render(request, 'blog/detail.html', context)


def category_page(request, slug):
    if slug == 'None':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = get_object_or_404(Category, slug=slug)
        post_list = Post.objects.filter(category=category)
        
    categories = Category.objects.all()
    no_category_post_count = Post.objects.filter(category=None).count()
    context = {'category':category, 'post_list':post_list, 'categories':categories, 'no_category_post_count':no_category_post_count}
    return render(request, 'blog/post_list.html', context)


def about(request):
    pass