# Generated by Django 4.2.7 on 2023-11-30 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Bookmark",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Краткое описание"
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата добавления"
                    ),
                ),
                (
                    "change_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Дата изменения"
                    ),
                ),
                (
                    "title",
                    models.TextField(
                        blank=True, null=True, verbose_name="Заголовок страницы"
                    ),
                ),
                (
                    "link",
                    models.URLField(max_length=512, verbose_name="Ссылка на страницу"),
                ),
                (
                    "link_type",
                    models.CharField(
                        choices=[
                            ("WS", "Website"),
                            ("BK", "Book"),
                            ("AR", "Article"),
                            ("MC", "Music"),
                            ("VD", "Video"),
                        ],
                        default="WS",
                        max_length=2,
                        verbose_name="Тип ссылки",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="img/",
                        verbose_name="Картинка превью",
                    ),
                ),
            ],
            options={
                "verbose_name": "Закладка",
                "verbose_name_plural": "Закладки",
                "ordering": ["-creation_date"],
            },
        ),
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Краткое описание"
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата добавления"
                    ),
                ),
                (
                    "change_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Дата изменения"
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Коллекция закладок",
                "verbose_name_plural": "Коллекции закладок",
                "ordering": ["-creation_date"],
            },
        ),
        migrations.CreateModel(
            name="CollectionBookmark",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "bookmark",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmark_collections",
                        to="bookmarks.bookmark",
                        verbose_name="Закладка",
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collection_bookmarks",
                        to="bookmarks.collection",
                        verbose_name="Коллекция",
                    ),
                ),
            ],
            options={
                "verbose_name": "Коллекция связана с закладкой",
                "verbose_name_plural": "Коллекции связанные с закладками",
            },
        ),
    ]