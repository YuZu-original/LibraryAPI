from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from library.models import Book, Reader, Author
from library.serializers import BookSerializer, ReaderSerializer, AuthorSerializer

@extend_schema(tags=['author'])
class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    tags = ['author']

@extend_schema(tags=['book'])
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    tags = ['book']

@extend_schema(tags=['reader'])
class ReaderViewSet(ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    tags = ['reader']
