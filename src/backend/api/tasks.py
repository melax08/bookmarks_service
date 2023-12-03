import logging

from bookmarks.models import Bookmark
from celery import shared_task

from .utils import get_information_from_link, save_image_from_url


@shared_task
def collect_link_information(bookmark_id, link):
    """Celery task, get information about specified link and save collected
    information to the model object."""

    try:
        link_information = get_information_from_link(link)
        bookmark = Bookmark.objects.get(pk=bookmark_id)

        link_type = link_information.pop("link_type", None)
        image_url = link_information.pop("image", None)

        try:
            bookmark.link_type = bookmark.LinkType[link_type].value
        except KeyError:
            pass

        if image_url:
            save_image_from_url(bookmark, image_url)

        for field, value in link_information.items():
            setattr(bookmark, field, value)

        if not Bookmark.objects.filter(pk=bookmark.id).exists():
            raise Bookmark.DoesNotExist

        bookmark.update_change_date()

    except Bookmark.DoesNotExist:
        logging.debug("Trying to access to the nonexistent model object.")
