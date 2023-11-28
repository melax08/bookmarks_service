from django.contrib import admin

from .models import Bookmark, CollectionBookmark, Collection

admin.site.register(Bookmark)
admin.site.register(CollectionBookmark)
admin.site.register(Collection)
