from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    # path('', index, name="index"),
    path('', BlogView.as_view(), name="index"),
    path('<int:pk>/', PostDetail.as_view(), name="detail"),
    path('post/<int:pk>/', PostDetail.as_view(), name="post"), # detail
    path('category/<str:slug>/', category_page, name="category"),
]
