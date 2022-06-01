from importlib.resources import path


from django.urls import path
from .views import *


app_name = 'lending'

urlpatterns = [
    path('', mainList, name="index"),
]
