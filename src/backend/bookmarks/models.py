from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Collection(BaseModel):
    """Collections model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="collections",
        verbose_name="Владелец коллекции",
    )
    title = models.CharField("Название", max_length=50)

    class Meta:
        verbose_name = "Коллекция закладок"
        verbose_name_plural = "Коллекции закладок"
        ordering = ["-creation_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_collection_title"
            )
        ]

    def __str__(self):
        return f"Коллекция закладок: {self.title}"


class Bookmark(BaseModel):
    """Bookmark model."""

    class LinkType(models.TextChoices):
        website = "WS"
        book = "BK"
        article = "AR"
        music = "MC"
        video = "VD"

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookmarks",
        verbose_name="Создатель закладки",
    )
    title = models.TextField("Заголовок страницы", null=True, blank=True)
    link = models.URLField("Ссылка на страницу", max_length=512)
    link_type = models.CharField(
        "Тип ссылки", max_length=2, choices=LinkType.choices, default="WS"
    )
    image = models.ImageField(
        "Картинка превью", upload_to="img/", null=True, blank=True
    )
    collections = models.ManyToManyField(
        Collection,
        through="CollectionBookmark",
        related_name="bookmarks",
        verbose_name="Коллекции",
    )

    class Meta:
        verbose_name = "Закладка"
        verbose_name_plural = "Закладки"
        ordering = ["-creation_date"]

    def __str__(self):
        return f"Закладка: {self.title}"


class CollectionBookmark(models.Model):
    """Through model of Collection and Bookmark models."""

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name="collection_bookmarks",
        verbose_name="Коллекция",
    )
    bookmark = models.ForeignKey(
        Bookmark,
        on_delete=models.CASCADE,
        related_name="bookmark_collections",
        verbose_name="Закладка",
    )

    class Meta:
        verbose_name = "Коллекция связана с закладкой"
        verbose_name_plural = "Коллекции связанные с закладками"

    def __str__(self):
        return (
            f"У закладки {self.bookmark.title} установлена коллекция "
            f"{self.collection.title}"
        )
