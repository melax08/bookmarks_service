from celery import shared_task

from bookmarks.models import Bookmark
from .utils import get_information_from_link


@shared_task
def collect_link_information(bookmark_id, link):
    link_information = get_information_from_link(link)
    bookmark = Bookmark.objects.get(pk=bookmark_id)

    link_type = link_information.pop('link_type', None)
    try:
        bookmark.link_type = bookmark.LinkType[link_type].value
    except KeyError:
        pass

    for field, value in link_information.items():
        setattr(bookmark, field, value)
    bookmark.save()
