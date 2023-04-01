from django.urls import path, include
from rest_framework.routers import DefaultRouter

from library import views

router = DefaultRouter()
router.register(r"author", views.AuthorViewSet)
router.register(r"book", views.BookViewSet)
router.register(r"reader", views.ReaderViewSet, basename="Reader")

urlpatterns = router.urls
