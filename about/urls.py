from importlib.resources import path
from pathlib import Path


from django.urls import path
from .views import *

app_name = 'about'

urlpatterns = [
    path('', about_me, name="about")
]
