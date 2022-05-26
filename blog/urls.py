from django.urls import path

from .views import *

app_name = 'blog'

urlpatterns = [
    path('', BlogView.as_view(), name="index"),
    path('<int:pk>/', PostDetail.as_view(), name="detail"),
    path('post/<int:pk>/', PostDetail.as_view(), name="post"), # detail
    path('category/<str:slug>/', category_page, name="category"),
    path('tag/<str:slug>/', tag_page, name="tag"),
    path('create_post/', PostCreate.as_view(), name="create_post"),
    path('update_post/<int:pk>/', PostUpdate.as_view(), name='post_update'),
    path('delete_post/<int:pk>/', PostDeleteView.as_view(), name="delete_post"),
]
