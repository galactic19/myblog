from django.db import models
from django.contrib.auth.models import User


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
    
    
    def get_absolute_url(self):
        return ''
    


class Post(models.Model):
    title = models.CharField(max_length=100)
    hook_title = models.CharField(max_length=50, blank=True)
    content = models.TextField()
    post_image = models.ImageField(upload_to='postImg/%Y/%m/%d', blank=True)
    post_file = models.FileField(upload_to='postFile/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 작성자
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # 카테고리
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)


    class Meta:
        ordering = ['-created_at']
        verbose_name = '포스트'
        verbose_name_plural = '포스트'


    def __str__(self):
        return self.title + " " + self.hook_title