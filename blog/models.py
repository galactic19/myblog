from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
import os


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    description = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = '카테고리'    
        verbose_name_plural = '카테고리'
    
    def __str__(self):
        return self.name
        # return self.name + self.slug

    def get_absolute_url(self):
        return reverse('blog:category', args=[self.slug])
        # return f'/blog/category/{self.slug}/'


class Tag(models.Model):
    name = models.CharField(max_length=50, db_index=True,)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'
    


class Post(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    hook_title = models.CharField(max_length=50, blank=True)
    content = models.TextField()
    post_image = models.ImageField(upload_to='postImg/%Y/%m/%d', blank=True)
    post_file = models.FileField(upload_to='postFile/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 작성자
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # 카테고리
    category = models.ForeignKey(Category, db_index=True, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, db_index=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '포스트'
        verbose_name_plural = '포스트'

    def __str__(self):
        return self.title + " " + self.hook_title
    

    def get_file_name(self):
        return os.path.basename(self.post_file.name)

    def get_file_size(self):
        file_path = "%s/%s" % (settings.MEDIA_ROOT, self.post_file.name)
        num_byte = os.path.getsize(file_path)
        result = num_byte/1024
        return int(result)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
    
    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.pk])
    
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f"https://doitdjango.com/avatar/id/1042/a0b7a0e8545d602a/svg/{self.author.email}"
    
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-modified_at', '-created_at']
    
    def __str__(self):
        return f'{self.author} :: {self.content}'
    
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
    
    #get_avatar_url
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f"https://doitdjango.com/avatar/id/1042/a0b7a0e8545d602a/svg/{self.author.email}"