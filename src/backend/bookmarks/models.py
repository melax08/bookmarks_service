from django.contrib.auth import get_user_model
from django.db import models
from core.models import BaseModel

User = get_user_model()

LINK_TYPES = (
    ('WS', 'website'),
    ('BK', 'book'),
    ('AR', 'article'),
    ('MC', 'music'),
    ('VD', 'video'),
)


class Collection(BaseModel):
    """Collections model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collections',
        verbose_name='Владелец коллекции'
    )
    title = models.CharField('Название', max_length=50)

    class Meta:
        verbose_name = 'Коллекция закладок'
        verbose_name_plural = 'Коллекции закладок'

    def __str__(self):
        return f'Коллекция закладок: {self.title}'


class Bookmark(BaseModel):
    """Bookmark model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='Создатель закладки'
    )
    title = models.TextField('Заголовок страницы', null=True, blank=True)
    link = models.URLField('Ссылка на страницу', max_length=512)
    link_type = models.CharField(
        'Тип ссылки', max_length=2, choices=LINK_TYPES, default='WS'
    )
    image = models.ImageField(
        'Картинка превью',
        upload_to='img/',
        null=True,
        blank=True
    )
    collections = models.ManyToManyField(
        Collection,
        through='CollectionBookmark',
        related_name='bookmarks',
        verbose_name='Коллекции'
    )

    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'

    def __str__(self):
        return f'Закладка: {self.title}'


class CollectionBookmark(models.Model):
    """Through model of Collection and Bookmark models."""

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name='collection_bookmarks',
        verbose_name='Коллекция'
    )
    bookmark = models.ForeignKey(
        Bookmark,
        on_delete=models.CASCADE,
        related_name='bookmark_collections',
        verbose_name='Закладка'
    )

    class Meta:
        verbose_name = 'Коллекция для закладки'
        verbose_name_plural = 'Коллекции для закладок'

    def __str__(self):
        return (
            f'У закладки {self.bookmark.title} установлена коллекция '
            f'{self.collection.title}'
        )
