from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookmarkViewSet, CollectionViewSet

app_name = "api"

router = DefaultRouter()
router.register("collections", CollectionViewSet, basename="collections")
router.register("bookmarks", BookmarkViewSet, basename="bookmarks")

urlpatterns = [path("", include(router.urls))]
