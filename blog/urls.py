from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', index, name="index"),
    path('<int:pk>', get_detail, name="detail"),
    path('post/<int:pk>', get_detail, name="post"), # detail
]
