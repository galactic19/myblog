from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    # path('', index, name="index"),
    path('', BlogView.as_view(), name="index"),
    path('<category_slug>/', BlogView.as_view(), name="index"), # slug 있을 때.
    path('<int:pk>', PostDetail.as_view(), name="detail"),
    path('post/<int:pk>', PostDetail.as_view(), name="post"), # detail
]
