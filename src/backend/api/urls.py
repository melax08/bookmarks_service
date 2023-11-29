from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import CollectionViewSet, BookmarkViewSet

app_name = 'api'

router = DefaultRouter()
router.register('collections', CollectionViewSet, basename='collections')
router.register('bookmarks', BookmarkViewSet, basename='bookmarks')

urlpatterns = [
    path('', include(router.urls))
]
