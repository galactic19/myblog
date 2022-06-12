from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from rest_framework import viewsets, permissions, generics, status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Book
from .serializers import BookSerializer



'''
    아래 클래스 뷰, 함수형 뷰의 중복점을 제거하여 다시 작성.
'''

class BooksAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
class BookAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self,request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


'''
    Class 형 View 를 generics 를 상속 받아 간결하게 작성.
'''
class BooksAPIGenerics(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class BookAPIGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'
    
    
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    

class BookList(ListView):
    model = Book


# @api_view(['GET', 'POST'])
# def booksAPI(request):
#     if request.method == 'GET':
#         books = Book.objects.all() # 모델에서 데이터 가져 오기.
#         serializer = BookSerializer(books, many=True) #시리얼라이저에 데이터 집어넣기(직렬화, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK) # return
    
#     elif request.method == 'POST' :
#         serializer = BookSerializer(data=request.data) # Post 요청으로 들어온 데이터를 시리얼라이즈에 넣기.
#         if serializer.is_valid(): # 유효한 정보가 넘어왔다면
#             serializer.save() # 모델시리얼라이저의 기본 create 함수가 동작.
#             return Response(serializer.data, status=status.HTTP_201_CREATED) # 201메세지 보내며 성공
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 잘못된 요청

# @api_view(['GET'])
# def bookAPI(request, bid):
#     book = get_object_or_404(Book, bid=bid)
#     serializer = BookSerializer(book)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# '''
#     class View 를 사용하여 위와 동일한 API 구성해 보기.
# '''

# class BooksAPI(APIView):
#     def get(self, request):
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def post(self, request):
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# class BookAPI(APIView):
#     def get(self, request, bid):
#         book = get_object_or_404(Book, bid=bid)
#         serializer = BookSerializer(book)
#         return Response(serializer.data, status=status.HTTP_200_OK)


