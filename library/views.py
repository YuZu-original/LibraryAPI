from django.contrib.auth.models import User
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from library.models import Book, Reader, Author
from library.permissions import ReaderAccessPermission, BaseObjectAccessPermission
from library.serializers import BookSerializer, ReaderSerializer, AuthorSerializer


@extend_schema(tags=["author"])
class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [BaseObjectAccessPermission]
    tags = ["author"]


@extend_schema(tags=["book"])
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [BaseObjectAccessPermission]
    tags = ["book"]


@extend_schema(tags=["reader"])
class ReaderViewSet(ModelViewSet):
    serializer_class = ReaderSerializer
    permission_classes = [ReaderAccessPermission]
    tags = ["reader"]

    def get_queryset(self):
        return Reader.objects.filter(user=self.request.user)
