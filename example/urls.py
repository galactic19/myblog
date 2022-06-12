from django.urls import path
from rest_framework import routers
from .views import *


app_name = 'book'


urlpatterns = [
    path('booklist/', BookList.as_view(), name="book_index"),
    # path('hello/', HelloAPI),
    # path('fbv/books/', booksAPI),
    # path('fbv/book/<int:bid>/', bookAPI),
    # path('cbv/books/', BooksAPI.as_view()),
    # path('cbv/book/<int:bid>/', BookAPI.as_view())
    path('mixin/books/', BooksAPIMixins.as_view()),
    path('mixin/book/<int:bid>/', BookAPIMixins.as_view()),
    path('generic/books/', BooksAPIGenerics.as_view()),
    path('generic/book/<int:bid>/', BookAPIGenerics.as_view()),
    # path('viewset/book/', BookViewSet.as_view()),
]
router = routers.SimpleRouter()
router.register('viewset/books', BookViewSet)
urlpatterns = router.urls