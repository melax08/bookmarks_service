from rest_framework import serializers

from bookmarks.models import Bookmark, Collection


class BookmarkCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ('id', 'link', 'collections', 'creation_date', 'change_date')
        read_only_fields = ('creation_date', 'change_date')


class BookmarkListRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        exclude = ('author',)


class BookmarkInCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        exclude = ('author', 'collections')


class CollectionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        exclude = ('author',)
        read_only_fields = ('creation_date', 'change_date')


class CollectionSerializer(serializers.ModelSerializer):
    bookmarks = BookmarkInCollectionSerializer(read_only=True, many=True)

    class Meta:
        model = Collection
        exclude = ('author',)
        read_only_fields = ('creation_date', 'change_date', 'bookmarks')
