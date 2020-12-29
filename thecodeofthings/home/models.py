from django.contrib.auth import models as auth_models
from django.db import models
from modelcluster import fields as modelcluster_fields
from modelcluster.contrib import taggit as modelcluster_taggit
from taggit import models as taggit_models
from wagtail.admin import edit_handlers as wagtail_panels
from wagtail.core import blocks as wagtail_blocks
from wagtail.core import fields as wagtail_fields
from wagtail.core import models as wagtail_models
from wagtail.images import blocks as wagtail_image_blocks
from wagtail.images import edit_handlers as wagtail_image_panels
from wagtail.snippets import models as snippet_models


# snippets
@snippet_models.register_snippet
class Line(models.Model):
    """
    Random poem line returned in the header.
    """

    text = models.CharField(max_length=500)
    is_published = models.BooleanField(blank=True, default=False)

    panels = [
        wagtail_panels.FieldPanel("text"),
        wagtail_panels.FieldPanel("is_published"),
    ]

    def __str__(self):
        return self.text


@snippet_models.register_snippet
class Quote(models.Model):
    """
    Random quote.
    """

    source = models.CharField(max_length=300)
    quote = models.TextField()
    citation = models.CharField(max_length=300)
    is_published = models.BooleanField(blank=True, default=False)

    panels = [
        wagtail_panels.FieldPanel("source"),
        wagtail_panels.FieldPanel("quote"),
        wagtail_panels.FieldPanel("citation"),
        wagtail_panels.FieldPanel("is_published"),
    ]

    def __str__(self):
        return f"{self.source}, {self.citation}"


@snippet_models.register_snippet
class Category(models.Model):
    """
    Category for posts and collections.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, allow_unicode=True, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(blank=True, default=0)

    panels = [
        wagtail_panels.FieldPanel("name"),
        wagtail_panels.FieldPanel("slug"),
        wagtail_panels.FieldPanel("description"),
        wagtail_panels.FieldPanel("order"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


# tags
class TaggedPost(taggit_models.TaggedItemBase):
    """
    A tag for a post.
    """

    content_object = modelcluster_fields.ParentalKey(
        "home.Post", related_name="tagged_posts", on_delete=models.CASCADE
    )


# blocks
class SectionBlock(wagtail_blocks.StructBlock):
    heading = wagtail_blocks.CharBlock()
    content = wagtail_blocks.RichTextBlock()


# pages
class HomePage(wagtail_models.Page):
    """
    The home page.
    """

    parent_page_types = []


class StandardPage(wagtail_models.Page):
    """
    A standard content page.
    """

    description = models.TextField(blank=True)
    extract = models.TextField(blank=True)
    authors = modelcluster_fields.ParentalManyToManyField(auth_models.User)
    date = models.DateTimeField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = wagtail_fields.StreamField(
        [
            ("heading", wagtail_blocks.CharBlock()),
            ("paragraph", wagtail_blocks.RichTextBlock()),
            ("section", SectionBlock()),
        ]
    )

    content_panels = wagtail_models.Page.content_panels + [
        wagtail_panels.FieldPanel("description"),
        wagtail_panels.FieldPanel("extract"),
        wagtail_panels.FieldPanel("authors"),
        wagtail_panels.FieldPanel("date"),
        wagtail_image_panels.ImageChooserPanel("featured_image"),
        wagtail_panels.StreamFieldPanel("body"),
    ]


class PostIndexPage(wagtail_models.Page):
    """
    A post index page.
    """

    subpage_types = ["home.Post"]


class Post(wagtail_models.Page):
    """
    A standard post.
    """

    description = models.TextField(blank=True)
    extract = models.TextField(blank=True)
    authors = modelcluster_fields.ParentalManyToManyField(auth_models.User)
    date = models.DateTimeField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    tags = modelcluster_taggit.ClusterTaggableManager(
        through="home.TaggedPost", blank=True
    )
    categories = modelcluster_fields.ParentalManyToManyField(
        "home.Category", blank=True
    )
    body = wagtail_fields.StreamField(
        [
            ("heading", wagtail_blocks.CharBlock()),
            ("paragraph", wagtail_blocks.RichTextBlock()),
            ("section", SectionBlock()),
            ("image", wagtail_image_blocks.ImageChooserBlock()),
        ]
    )

    content_panels = wagtail_models.Page.content_panels + [
        wagtail_panels.FieldPanel("description"),
        wagtail_panels.FieldPanel("extract"),
        wagtail_panels.FieldPanel("authors"),
        wagtail_panels.FieldPanel("date"),
        wagtail_panels.FieldPanel("tags"),
        wagtail_panels.FieldPanel("categories"),
        wagtail_image_panels.ImageChooserPanel("featured_image"),
        wagtail_panels.StreamFieldPanel("body"),
    ]

    parent_page_types = ["home.PostIndexPage"]
    subpage_types = []
