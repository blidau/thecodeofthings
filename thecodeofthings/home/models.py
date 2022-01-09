from django.db import models
from wagtail.admin import edit_handlers as wagtail_panels
from wagtail.core import models as wagtail_models
from wagtail.snippets import models as wagtail_snippet_models

from blog import models as blog_models
from poems import models as poems_models


# snippets
@wagtail_snippet_models.register_snippet
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


@wagtail_snippet_models.register_snippet
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


# pages
class HomePage(wagtail_models.Page):
    """
    The home page.
    """

    parent_page_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["about_page"] = blog_models.StandardPage.objects.live().public().filter(title="About").first()
        context["poem"] = poems_models.PoemPage.objects.live().public().order_by("-date_created").first()
        return context
