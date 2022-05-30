from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CommentForm, PostCreateForm

import re

from .models import *


class BlogView(ListView):
    model = Post
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['category'] = '전체 게시물'
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['post_list'] = Post.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    # fields = ['title', 'hook_title', 'content', 'post_image', 'post_file', 'category']
    form_class = PostCreateForm

    def test_func(self):
        # return self.request.user.is_authenticated
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):  # form inser 할 때 진입 되고 있음.
        current_user = self.request.user

        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            # if current_user.is_authenticated: # 관리자 아닌 로그인 유저 모두가 글을 쓸수있게 하고 싶었음.
            form.instance.author = current_user
            response = super().form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.rstrip(';,')
                tags_str = tags_str.lstrip(';,')
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_str = tags_str.split(';')

                for t in tags_str:
                    t = t.strip()
                    t = re.sub(r'[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', t)  # 정규식으로 문자열의 특수문자를 제거

                    tag, is_tag_created = Tag.objects.get_or_create(name=t)

                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return PermissionDenied
            # return redirect('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head_title"] = ' Create New Post'
        context['create_form'] = PostCreateForm
        return context


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    # fields = ['title','hook_title', 'content', 'post_image', 'post_file', 'category']
    form_class = PostCreateForm

    def dispatch(self, request, *args, **kwargs):
        '''
            dispatch 메서드는 사용자가 get/post 방식으로 요청 했는지를 판단하는 메서드
            CreateView, UpdateView 에서 사용한다.
        '''
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        # form = PostCreateForm(self.request.POST.get('pk'))
        response = super().form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.rstrip(';,')
            tags_str = tags_str.lstrip(';,')
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                t = re.sub(r'[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', t)  # 정규식으로 문자열의 특수문자를 제거

                tag, is_tag_created = Tag.objects.get_or_create(name=t)

                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()

                self.object.tags.add(tag)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.tags.exists():
            tags_str_list = []

            for i in self.object.tags.all():
                tags_str_list.append(i.name)
            context['tags_str_default'] = '; '.join(tags_str_list)

        context["head_title"] = ' Edit Post'
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/blog/'


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            # return super().dispatch(request, *args, **kwargs)
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/post_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)

        else:
            raise PermissionDenied

    def form_valid(self, form):
        '''
            Class 형 View 에서 삭제 후 해당 페이지로 돌려주기 위해 form_valid 를 오버라이드해 redirect 처리 했다.
            삭제 할 것이기 때문에 super()의  값은 상속 받지 않았다.
            form_valid에 들어가 보니 success_url 이 자리 잡고 있었기에 form_valid 를 오버라이드 했다.
            도서에서는 함수형 view 를 만들어 삭제 처리 했다.
        '''
        success_url = f"/blog/{self.object.post.pk}/"
        self.object.delete()
        return HttpResponseRedirect(success_url)
        # return redirect(success_url) # 두가지 차이점은 뭐지.


# 함수형 View 로 댓글 삭제를 구현 할 때.
# 함수형 View 를 사용한다면 Class View 를 사용할 때 삭제 confirm 을 받는 페이지를 건너 뛸 수 있다. 그래서 팝업으로 작동 시킬 수 있다.
# def delete_comment(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     post = comment.post
#     if request.user.is_authenticated and request.user == comment.author:
#         comment.delete()
#         return redirect(post.get_absolute_url())
#     else:
#         raise PermissionDenied


def category_page(request, slug):
    if slug == 'None':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = get_object_or_404(Category, slug=slug)
        post_list = Post.objects.filter(category=category)

    post_list.count = Post.objects.count()
    categories = Category.objects.all()
    no_category_post_count = Post.objects.filter(category=None).count()
    context = {'category': category, 'post_list': post_list, 'categories': categories,
               'no_category_post_count': no_category_post_count}
    return render(request, 'blog/post_list.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    post_list.count = Post.objects.count()
    categories = Category.objects.all()
    no_category_post_count = Post.objects.filter(category=None).count()
    context = {'tag': tag, 'post_list': post_list, 'categories': categories,
               'no_category_post_count': no_category_post_count}
    return render(request, 'blog/post_list.html', context)


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
            else:
                return redirect(post.get_absolute_url())
        else:
            raise PermissionDenied
