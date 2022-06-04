from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import *

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['bid','title','creator', 'category', 'pages', 'price', 'published_date', 'description']