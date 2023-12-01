from django.contrib import admin

from .models import Bookmark, Collection, CollectionBookmark


class CollectionInlineAdmin(admin.TabularInline):
    model = Bookmark.collections.through


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "description", "link", "link_type", "author")
    list_filter = ("author", "link_type")
    inlines = [CollectionInlineAdmin]


class CollectionAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "description", "author")


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(CollectionBookmark)
admin.site.register(Collection, CollectionAdmin)
