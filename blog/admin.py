from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at', 'updated_at', 'author']
    search_fields = ['title']
    list_per_page = 8


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
    
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}
    list_per_page= 10
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'created_at', 'author']
    list_per_page= 10