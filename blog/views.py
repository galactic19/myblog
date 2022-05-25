from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .models import *


class BlogView(ListView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = len(Post.objects.filter(category=None))
        context['category'] = '전체 게시물'
        return context        


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['post_list'] = Post.objects.all()
        context['no_category_post_count'] = len(Post.objects.filter(category=None))
        return context        


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_title', 'content', 'post_image', 'post_file', 'category']
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form): # form inser 할 때 진입 되고 있음.
        current_user = self.request.user
        
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super().form_valid(form)
            
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                
                tags_str = tags_str.replace(',', ';')
                tags_str = tags_str.split(';')
                
                for t in tags_str:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head_title"] = ' Create New Post'
        return context
    


class PostUpdate(LoginRequiredMixin, UpdateView):
        model = Post
        fields = ['title','hook_title', 'content', 'post_image', 'post_file', 'category', 'tags']

        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated and request.user == self.get_object().author:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied
            
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["head_title"] = ' Edit Post'
            return context
        


def category_page(request, slug):
    if slug == 'None':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = get_object_or_404(Category, slug=slug)
        post_list = Post.objects.filter(category=category)

    post_list.count = len(Post.objects.all())
    categories = Category.objects.all()
    no_category_post_count = len(Post.objects.filter(category=None))
    context = {'category':category, 'post_list':post_list, 'categories':categories, 'no_category_post_count':no_category_post_count}
    return render(request, 'blog/post_list.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    post_list.count = len(Post.objects.all())
    categories = Category.objects.all()
    no_category_post_count = len(Post.objects.filter(category=None))
    context = {'tag':tag, 'post_list':post_list, 'categories':categories, 'no_category_post_count':no_category_post_count}
    return render(request, 'blog/post_list.html', context)
