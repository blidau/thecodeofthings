from django.db import models
from modelcluster import fields as modelcluster_fields
from wagtail.admin import edit_handlers as wagtail_panels
from wagtail.core import blocks as wagtail_blocks
from wagtail.core import fields as wagtail_fields
from wagtail.core import models as wagtail_models
from wagtail.images import blocks as wagtail_image_blocks
from wagtail.images import edit_handlers as wagtail_image_panels
from wagtail.snippets import models as wagtail_snippet_models


# snippets
@wagtail_snippet_models.register_snippet
class Medium(models.Model):
    """
    Medium for poems.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, allow_unicode=True, unique=True)
    description = models.TextField(blank=True)

    panels = [
        wagtail_panels.FieldPanel("name"),
        wagtail_panels.FieldPanel("slug"),
        wagtail_panels.FieldPanel("description"),
    ]

    def __str__(self):
        return self.name


# blocks
class VersionBlock(wagtail_blocks.StructBlock):
    """
    Poem version block.
    """

    title = wagtail_blocks.CharBlock()
    description = wagtail_blocks.RichTextBlock()
    featured_image = wagtail_image_blocks.ImageChooserBlock(required=False)
    date_created = wagtail_blocks.DateTimeBlock()
    date_released = wagtail_blocks.DateTimeBlock(required=False)
    date_modified = wagtail_blocks.DateTimeBlock(required=False)
    link = wagtail_blocks.URLBlock(required=False)

    class Meta:
        icon = "doc-empty"
        template = "poems/blocks/version.html"


# pages
class PoemPage(wagtail_models.Page):
    """
    A poem page.
    """

    description = wagtail_fields.RichTextField(blank=True)
    authors = modelcluster_fields.ParentalManyToManyField("users.User")
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    mediums = modelcluster_fields.ParentalManyToManyField("poems.Medium", blank=True)
    repository = models.URLField(blank=True)
    versions = wagtail_fields.StreamField(
        [
            ("version", VersionBlock()),
        ],
        blank=True,
    )

    content_panels = wagtail_models.Page.content_panels + [
        wagtail_panels.FieldPanel("description"),
        wagtail_image_panels.ImageChooserPanel("featured_image"),
        wagtail_panels.FieldPanel("authors"),
        wagtail_panels.FieldPanel("date_created"),
        wagtail_panels.FieldPanel("date_modified"),
        wagtail_panels.FieldPanel("mediums"),
        wagtail_panels.FieldPanel("repository"),
        wagtail_panels.StreamFieldPanel("versions"),
    ]

    parent_page_types = ["poems.PoemIndexPage"]
    subpage_types = []


class PoemIndexPage(wagtail_models.Page):
    """
    A poem index page.
    """

    date_created = models.DateTimeField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = wagtail_models.Page.content_panels + [
        wagtail_image_panels.ImageChooserPanel("featured_image"),
        wagtail_panels.FieldPanel("date_created"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["poems.PoemPage"]
