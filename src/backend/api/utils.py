import logging
import urllib.error
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse
from urllib.request import urlopen

import metadata_parser
from django.core.files import File
from django.utils.crypto import get_random_string
from PIL import Image, UnidentifiedImageError


def get_information_from_link(link):
    """Parse Open Graph information or mata information for the specified link."""
    try:
        page = metadata_parser.MetadataParser(url=link)
        metadata = page.metadata
        return {
            "title": (
                metadata.get("og").get("title") or metadata.get("page").get("title")
            ),
            "description": (
                metadata.get("og").get("description")
                or metadata.get("meta").get("description")
            ),
            "link_type": metadata.get("og").get("type") or None,
            "image": metadata.get("og").get("image") or None,
        }
    except metadata_parser.NotParsableFetchError:
        return {}


def save_image_from_url(obj, url):
    """
    Tries to get an image from the provided link.
    If successful, then puts it in the model object image field.
    """
    try:
        temp_img = NamedTemporaryFile(delete=True)
        temp_img.write(urlopen(url).read())
        temp_img.flush()

        Image.open(temp_img)

        ext = urlparse(url).path.split(".")[-1]
        obj.image.save(f"{get_random_string(length=32)}.{ext}", File(temp_img))
    except (ValueError, urllib.error.URLError, UnidentifiedImageError):
        logging.info(f"There is something wrong with the image in the link: {url}")
