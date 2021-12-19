import datetime

from django import shortcuts
from django.core import paginator
from django.db import models
from modelcluster import fields as modelcluster_fields
from modelcluster.contrib import taggit as modelcluster_taggit
from taggit import models as taggit_models
from wagtail.admin import edit_handlers as wagtail_panels
from wagtail.contrib.routable_page import models as routable_models
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
    excerpt = wagtail_fields.RichTextField(blank=True)
    authors = modelcluster_fields.ParentalManyToManyField("users.User")
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
        wagtail_panels.FieldPanel("excerpt"),
        wagtail_panels.FieldPanel("authors"),
        wagtail_panels.FieldPanel("date"),
        wagtail_image_panels.ImageChooserPanel("featured_image"),
        wagtail_panels.StreamFieldPanel("body"),
    ]


class Post(wagtail_models.Page):
    """
    A standard post.
    """

    description = models.TextField(blank=True)
    excerpt = wagtail_fields.RichTextField(blank=True)
    authors = modelcluster_fields.ParentalManyToManyField("users.User")
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
        wagtail_panels.FieldPanel("excerpt"),
        wagtail_panels.FieldPanel("authors"),
        wagtail_panels.FieldPanel("date"),
        wagtail_panels.FieldPanel("tags"),
        wagtail_panels.FieldPanel("categories"),
        wagtail_image_panels.ImageChooserPanel("featured_image"),
        wagtail_panels.StreamFieldPanel("body"),
    ]

    parent_page_types = ["home.PostIndexPage"]
    subpage_types = []

    def set_url_path(self, parent):
        super().set_url_path(parent=parent)
        self.url_path = self.url_path.replace(
            self.slug, f"{self.date:%Y/%b/%d/}{self.slug}".lower()
        )


class PostIndexPage(routable_models.RoutablePageMixin, wagtail_models.Page):
    """
    A post index page.
    """

    subpage_types = ["home.Post"]

    def get_posts(self):
        return Post.objects.descendant_of(self).live().order_by('-date')

    @routable_models.route(r'^$')
    def view_posts(self, request):
        post_paginator = paginator.Paginator(self.get_posts(), 5)
        posts_page = request.GET.get("page")
        try:
            posts = post_paginator.page(posts_page)
        except paginator.PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = post_paginator.page(1)
        except paginator.EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = post_paginator.page(post_paginator.num_pages)

        return self.render(request, context_overrides={
            "title": "Posts",
            "posts": posts,
        })

    @routable_models.route(r"^(?P<year>\d{4})/?$")
    @routable_models.route(r"^(?P<year>\d{4})/(?P<month>(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))/?$")
    @routable_models.route(
        r"^(?P<year>\d{4})/(?P<month>(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))/(?P<day>\d{2})/?$"
    )
    def view_posts_by_date(self, request, year, month=None, day=None):
        title = f"Posts for {year}"
        filtered_posts = self.get_posts().filter(
            date__year=year,
        )
        if month:
            title = f"Posts for {datetime.datetime.strptime(month, '%b').strftime('%B')} {year}"
            filtered_posts = filtered_posts.filter(
                date__month=datetime.datetime.strptime(month, "%b").month,
            )
        if day:
            title = f"Posts for {int(day)} {datetime.datetime.strptime(month, '%b').strftime('%B')} {year}"
            filtered_posts = filtered_posts.filter(
                date__month=datetime.datetime.strptime(month, "%b").month,
            )

        post_paginator = paginator.Paginator(filtered_posts, 5)
        posts_page = request.GET.get("page")
        try:
            posts = post_paginator.page(posts_page)
        except paginator.PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = post_paginator.page(1)
        except paginator.EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = post_paginator.page(post_paginator.num_pages)
        return self.render(request, context_overrides={
            "title": title,
            "posts": posts,
        })

    @routable_models.route(r"^tag/(?P<tag_slug>[\w-]+)/?$")
    def view_posts_by_tag(self, request, tag_slug):
        tag = shortcuts.get_object_or_404(
            taggit_models.Tag,
            slug=tag_slug,
        )
        posts = self.get_posts().filter(
            tags=tag,
        )
        title = f"Posts for tag | {tag.name}"
        return self.render(request, context_overrides={
            "title": title,
            "posts": posts,
        })

    @routable_models.route(r"^category/(?P<category_slug>[\w-]+)/?$")
    def view_posts_by_category(self, request, category_slug):
        category = shortcuts.get_object_or_404(
            Category,
            slug=category_slug
        )
        posts = self.get_posts().filter(
            categories=category,
        )
        title = f"Posts for category | {category.name}"
        return self.render(request, context_overrides={
            "title": title,
            "posts": posts,
        })

    @routable_models.route(
        r"^(?P<year>\d{4})/(?P<month>(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))"
        r"/(?P<day>\d{2})/(?P<post_slug>[\w-]+)/?$"
    )
    def view_post_by_date_and_slug(self, request, year, month, day, post_slug):
        post = shortcuts.get_object_or_404(
            self.get_posts(),
            date__year=year,
            date__month=datetime.datetime.strptime(month, "%b").month,
            date__day=day,
            slug=post_slug
        )
        return post.serve(request)
