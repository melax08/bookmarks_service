from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from django.utils import timezone

from bookmarks.models import Collection, Bookmark, CollectionBookmark
from .serializers import CollectionSerializer, BookmarkSerializer


class BaseViewSet(ModelViewSet):
    model = ...

    def get_queryset(self):
        return self.model.objects.select_related('author').filter(
            author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user,
            change_date=timezone.now()
        )


class CollectionViewSet(BaseViewSet):
    serializer_class = CollectionSerializer
    model = Collection

    @action(detail=True, methods=['post'])
    def add_bookmark(self, request, pk=None):
        collection = self.get_object()
        bookmark = self._get_bookmark(request)

        if not CollectionBookmark.objects.filter(
                collection=collection, bookmark=bookmark
        ):
            CollectionBookmark.objects.create(
                collection=collection,
                bookmark=bookmark
            )
            return Response(
                self.get_serializer(collection).data,
                status=status.HTTP_201_CREATED
            )

        raise ValidationError(
            {'bookmark_id': 'Данная закладка уже добавлена в коллекцию'}
        )

    @action(detail=True, methods=['post'])
    def delete_bookmark(self, request, pk=None):
        collection = self.get_object()
        bookmark = self._get_bookmark(request)

        bookmark_in_collection = CollectionBookmark.objects.filter(
            collection=collection, bookmark=bookmark)
        if bookmark_in_collection.exists():
            bookmark_in_collection.first().delete()
            return Response(
                self.get_serializer(collection).data,
                status=status.HTTP_200_OK
            )

        raise ValidationError(
            {'bookmark_id': 'Данная закладка отсутствует в коллекции'}
        )

    def _get_bookmark(self, request):
        bookmark_id = request.data.get('bookmark_id')

        if bookmark_id is None or not isinstance(bookmark_id, int):
            raise ValidationError(
                {'bookmark_id': 'id закладки указан некорректно или не указан вовсе'}
            )

        bookmark = Bookmark.objects.filter(pk=bookmark_id, author=request.user)
        if not bookmark:
            raise ValidationError(
                {'bookmark_id': 'Предоставленная закладка не существует'}
            )
        return bookmark.first()


class BookmarkViewSet(BaseViewSet):
    serializer_class = BookmarkSerializer
    model = Bookmark
    http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer):
        super().perform_create(serializer)
        ...  # Тут добавление задачи по извлечению информации из URL в очередь
