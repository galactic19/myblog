from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *


class BlogView(ListView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context        


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['post_list'] = Post.objects.all()
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


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    categories = Category.objects.all()
    no_category_post_count = Post.objects.filter(category=None).count()
    context = {'tag':tag, 'post_list':post_list, 'categories':categories, 'no_category_post_count':no_category_post_count}
    return render(request, 'blog/post_list.html', context)



class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_title', 'content', 'post_image', 'post_file', 'category']
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form): # form inser 할 때 진입 되고 있음.
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            print('form_valid 엘스로  진입 했습니다.')
            return redirect('blog:index')

def about(request):
    pass