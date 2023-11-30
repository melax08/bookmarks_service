from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema

from bookmarks.models import Collection, Bookmark, CollectionBookmark
from .serializers import (
    BookmarkCreateSerializer,
    BookmarkListRetrieveSerializer,
    CollectionSerializer,
    CollectionListSerializer,
)
from .tasks import collect_link_information
from .open_api import (
    add_delete_bookmark_collection_body,
    add_bookmark_responses,
    delete_bookmark_response,
    add_new_bookmark_description,
)


class BaseViewSet(ModelViewSet):
    """
    Base ViewSet with implemented perform_create and perform_update methods.
    Only for inheritance.
    """

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user, change_date=timezone.now())


class CollectionViewSet(BaseViewSet):
    """
    ViewSet working with Collection model.
    Extra actions:
    - add_bookmark - to add a bookmark to the collection.
    - delete_bookmark - to delete a bookmark from the collection.
    """

    def get_queryset(self):
        return (
            Collection.objects.select_related("author")
            .prefetch_related("collection_bookmarks")
            .filter(author=self.request.user)
        )

    def get_serializer_class(self):
        if self.action in ("create", "list"):
            return CollectionListSerializer

        return CollectionSerializer

    @swagger_auto_schema(
        responses=add_bookmark_responses,
        request_body=add_delete_bookmark_collection_body,
    )
    @action(detail=True, methods=["post"])
    def add_bookmark(self, request, pk=None):
        """Add the bookmark to the collection."""
        collection = self.get_object()
        bookmark = self._get_bookmark(request)

        if not CollectionBookmark.objects.filter(
            collection=collection, bookmark=bookmark
        ):
            CollectionBookmark.objects.create(collection=collection, bookmark=bookmark)

            self._update_change_time(collection, bookmark)

            return Response(
                self.get_serializer(collection).data, status=status.HTTP_201_CREATED
            )

        raise ValidationError(
            {"bookmark_id": "Данная закладка уже добавлена в коллекцию"}
        )

    @swagger_auto_schema(
        responses=delete_bookmark_response,
        request_body=add_delete_bookmark_collection_body,
    )
    @action(detail=True, methods=["post"])
    def delete_bookmark(self, request, pk=None):
        """Delete the bookmark from the collection."""
        collection = self.get_object()
        bookmark = self._get_bookmark(request)

        bookmark_in_collection = CollectionBookmark.objects.filter(
            collection=collection, bookmark=bookmark
        )
        if bookmark_in_collection.exists():
            bookmark_in_collection.first().delete()

            self._update_change_time(collection, bookmark)

            return Response(
                self.get_serializer(collection).data, status=status.HTTP_200_OK
            )

        raise ValidationError(
            {"bookmark_id": "Данная закладка отсутствует в коллекции"}
        )

    @staticmethod
    def _get_bookmark(request):
        """Validate the bookmark_id request data parameter
        and return a Bookmark object."""

        bookmark_id = request.data.get("bookmark_id")

        if bookmark_id is None or not isinstance(bookmark_id, int):
            raise ValidationError(
                {"bookmark_id": "id закладки указан некорректно или не указан вовсе"}
            )

        bookmark = Bookmark.objects.filter(pk=bookmark_id, author=request.user)
        if not bookmark:
            raise ValidationError(
                {"bookmark_id": "Предоставленная закладка не существует"}
            )
        return bookmark.first()

    @staticmethod
    def _update_change_time(*args):
        """Update change_date field to current time for specified objects."""
        for obj in args:
            obj.update_change_date()


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description=add_new_bookmark_description,
        request_body=BookmarkCreateSerializer,
    ),
)
class BookmarkViewSet(BaseViewSet):
    """ViewSet working with Bookmark model."""

    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return (
            Bookmark.objects.select_related("author")
            .prefetch_related("bookmark_collections")
            .filter(author=self.request.user)
        )

    def get_serializer_class(self):
        if self.action == "create":
            return BookmarkCreateSerializer

        return BookmarkListRetrieveSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        collect_link_information.delay(
            serializer.data.get("id"), serializer.data.get("link")
        )
