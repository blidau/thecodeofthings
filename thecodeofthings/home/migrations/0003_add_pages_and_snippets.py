# Generated by Django 3.2.10 on 2022-01-03 04:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.contrib.routable_page.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0023_add_choose_permissions"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wagtailcore", "0066_collection_management_permissions"),
        ("taggit", "0003_taggeditem_add_unique_index"),
        ("home", "0002_create_homepage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=100)),
                (
                    "slug",
                    models.SlugField(allow_unicode=True, max_length=100, unique=True),
                ),
                ("description", models.TextField(blank=True)),
                ("order", models.PositiveSmallIntegerField(blank=True, default=0)),
            ],
            options={
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="Line",
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
                ("text", models.CharField(max_length=500)),
                ("is_published", models.BooleanField(blank=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("excerpt", wagtail.core.fields.RichTextField(blank=True)),
                ("date", models.DateTimeField()),
                (
                    "body",
                    wagtail.core.fields.StreamField(
                        [
                            ("heading", wagtail.core.blocks.CharBlock()),
                            ("paragraph", wagtail.core.blocks.RichTextBlock()),
                            (
                                "section",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        ("heading", wagtail.core.blocks.CharBlock()),
                                        (
                                            "content",
                                            wagtail.core.blocks.RichTextBlock(),
                                        ),
                                    ]
                                ),
                            ),
                            ("image", wagtail.images.blocks.ImageChooserBlock()),
                        ]
                    ),
                ),
                (
                    "authors",
                    modelcluster.fields.ParentalManyToManyField(to=settings.AUTH_USER_MODEL),
                ),
                (
                    "categories",
                    modelcluster.fields.ParentalManyToManyField(blank=True, to="home.Category"),
                ),
                (
                    "featured_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="Quote",
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
                ("source", models.CharField(max_length=300)),
                ("quote", models.TextField()),
                ("citation", models.CharField(max_length=300)),
                ("is_published", models.BooleanField(blank=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name="TaggedPost",
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
                    "content_object",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tagged_posts",
                        to="home.post",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="home_taggedpost_items",
                        to="taggit.tag",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="StandardPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("excerpt", wagtail.core.fields.RichTextField(blank=True)),
                ("date", models.DateTimeField()),
                (
                    "body",
                    wagtail.core.fields.StreamField(
                        [
                            ("heading", wagtail.core.blocks.CharBlock()),
                            ("paragraph", wagtail.core.blocks.RichTextBlock()),
                            (
                                "section",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        ("heading", wagtail.core.blocks.CharBlock()),
                                        (
                                            "content",
                                            wagtail.core.blocks.RichTextBlock(),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                (
                    "authors",
                    modelcluster.fields.ParentalManyToManyField(to=settings.AUTH_USER_MODEL),
                ),
                (
                    "featured_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="PostIndexPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("date_created", models.DateTimeField()),
                (
                    "featured_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtail.contrib.routable_page.models.RoutablePageMixin,
                "wagtailcore.page",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=modelcluster.contrib.taggit.ClusterTaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="home.TaggedPost",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
