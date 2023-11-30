from django.utils import timezone
from django.db import models


class BaseModel(models.Model):
    """Abstract model with base fields."""

    description = models.TextField('Краткое описание', blank=True, null=True)
    creation_date = models.DateTimeField('Дата добавления', auto_now_add=True)
    change_date = models.DateTimeField('Дата изменения', blank=True, null=True)

    class Meta:
        abstract = True

    def update_change_date(self):
        """Update change datetime to current datetime."""
        self.change_date = timezone.now()
        self.save()
