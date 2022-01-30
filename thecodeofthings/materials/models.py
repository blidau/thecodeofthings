from django import http
from django.db import models
from wagtail.admin import edit_handlers as wagtail_panels
from wagtail.core import models as wagtail_models
from wagtail.images import edit_handlers as wagtail_image_panels


class MaterialIndexPage(wagtail_models.Page):
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
    subpage_types = ["references.ReferenceIndexPage"]

    def serve(self, request, *args, **kwargs):
        first_child = self.get_children().live().public().first()
        return http.HttpResponseRedirect(first_child.full_url)
