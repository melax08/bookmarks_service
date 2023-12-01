from bookmarks.models import Bookmark, Collection
from rest_framework import serializers


class BookmarkCreateSerializer(serializers.ModelSerializer):
    """Bookmark model serializer for the `create` action."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_collections = Collection.objects.select_related("author").filter(
            author=self._user
        )
        self.fields["collections"] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=user_collections, required=False
        )

    @property
    def _user(self):
        """Get request user from request context."""
        request = self.context.get("request", None)
        if request:
            return request.user

    class Meta:
        model = Bookmark
        fields = ("id", "link", "collections", "creation_date", "change_date")
        read_only_fields = ("creation_date", "change_date")


class BookmarkListRetrieveSerializer(serializers.ModelSerializer):
    """Bookmark model serializer for the `retrieve` and `list` actions."""

    class Meta:
        model = Bookmark
        exclude = ("author",)


class BookmarkInCollectionSerializer(serializers.ModelSerializer):
    """Nested Bookmark model serializer for collection views."""

    class Meta:
        model = Bookmark
        exclude = ("author", "collections")


class CollectionListSerializer(serializers.ModelSerializer):
    """Collection model serializer for the `list` and `create` actions."""

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Collection
        fields = "__all__"
        read_only_fields = ("creation_date", "change_date")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Collection.objects.select_related("author").all(),
                fields=("author", "title"),
            )
        ]


class CollectionSerializer(serializers.ModelSerializer):
    """Collection model serializer with bookmarks field."""

    bookmarks = BookmarkInCollectionSerializer(read_only=True, many=True)

    class Meta:
        model = Collection
        exclude = ("author",)
        read_only_fields = ("creation_date", "change_date", "bookmarks")
