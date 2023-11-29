from rest_framework import serializers

from bookmarks.models import Bookmark, Collection


class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ('id', 'link', 'collections')


class CollectionSerializer(serializers.ModelSerializer):
    bookmarks = BookmarkSerializer(read_only=True, many=True)

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ('author', 'creation_date', 'change_date', 'bookmarks')
