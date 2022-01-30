from django import shortcuts
from django.core import paginator
from django.db import models
from wagtail.admin import edit_handlers as wagtail_panels
from wagtail.contrib.routable_page import models as routable_models
from wagtail.core import models as wagtail_models
from wagtail.images import edit_handlers as wagtail_image_panels


class Collection(models.Model):
    """
    A collection.
    """

    key = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    category = models.OneToOneField("blog.Category", null=True, on_delete=models.SET_NULL)
    hidden = models.BooleanField(blank=True, default=False)
    research = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["category__order", "name"]


class Creator(models.Model):
    """
    A reference creator.
    """

    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=400, blank=True, unique=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["first_name", "last_name"], name="unique_creator_name")]
        ordering = ("last_name", "first_name")

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name

    def get_full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.first_name


class ReferenceType(models.TextChoices):
    """
    Type of reference.
    """

    ARTWORK = "artwork", "Artwork"
    AUDIORECORDING = "audioRecording", "Audio Recording"
    BILL = "bill", "Bill"
    BLOGPOST = "blogPost", "Blog Post"
    BOOK = "book", "Book"
    BOOKSECTION = "bookSection", "Book Section"
    CASE = "case", "Case"
    COMPUTERPROGRAM = "computerProgram", "Computer Program"
    CONFERENCEPAPER = "conferencePaper", "Conference Paper"
    DICTIONARYENTRY = "dictionaryEntry", "Dictionary Entry"
    DOCUMENT = "document", "Document"
    EMAIL = "email", "E-mail"
    ENCYCLOPEDIAARTICLE = "encyclopediaArticle", "Encyclopedia Article"
    FILM = "film", "Film"
    FORUMPOST = "forumPost", "Forum Post"
    HEARING = "hearing", "Hearing"
    INSTANTMESSAGE = "instantMessage", "Instant Message"
    INTERVIEW = "interview", "Interview"
    JOURNALARTICLE = "journalArticle", "Journal Article"
    LETTER = "letter", "Letter"
    MAGAZINEARTICLE = "magazineArticle", "Magazine Article"
    MANUSCRIPT = "manuscript", "Manuscript"
    MAP = "map", "Map"
    NEWSPAPERARTICLE = "newspaperArticle", "Newspaper Article"
    PATENT = "patent", "Patent"
    PODCAST = "podcast", "Podcast"
    PRESENTATION = "presentation", "Presentation"
    RADIOBROADCAST = "radioBroadcast", "Radio Broadcast"
    REPORT = "report", "Report"
    STATUTE = "statute", "Statute"
    TVBROADCAST = "tvBroadcast", "TV Broadcast"
    THESIS = "thesis", "Thesis"
    VIDEORECORDING = "videoRecording", "Video Recording"
    WEBPAGE = "webpage", "Web Page"


class Reference(models.Model):
    """
    A reference.
    """

    key = models.CharField(max_length=20, primary_key=True)
    version = models.PositiveIntegerField(null=True, blank=True)
    item_type = models.CharField(max_length=30, choices=ReferenceType.choices)
    creators = models.ManyToManyField("Creator", through="Role", blank=True)
    collections = models.ManyToManyField("Collection", blank=True)
    title = models.CharField(max_length=500)
    short_title = models.CharField(max_length=200, blank=True)
    abstract_note = models.TextField(blank=True)
    date = models.CharField(max_length=200, blank=True)  # Irregular formats so kept as charfield
    url = models.URLField(blank=True)
    date_added = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=20, blank=True)
    rights = models.CharField(max_length=200, blank=True)
    extra = models.TextField(blank=True)
    additional = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    A creator reference role.
    """

    creator = models.ForeignKey("Creator", on_delete=models.CASCADE)
    reference = models.ForeignKey("Reference", on_delete=models.CASCADE)
    title = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["creator", "reference", "title"], name="unique_creator_reference_title")
        ]
        ordering = ["title"]

    def __str__(self):
        return f"{self.creator} {self.title} {self.reference}"


class ReferenceIndexPage(routable_models.RoutablePageMixin, wagtail_models.Page):
    """
    A reference index page.
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
    subpage_types = []

    @routable_models.route(r"^$")
    @routable_models.route(r"^collections/(?P<category_slug>[\w-]+)/$")
    @routable_models.route(r"^collections/(?P<category_slug>[\w-]+)/(?P<first_filter>[\w-]+)/$")
    @routable_models.route(
        r"^collections/(?P<category_slug>[\w-]+)/(?P<first_filter>[\w-]+)/(?P<second_filter>[\w-]+)/$"
    )
    @routable_models.route(r"^collections/creators/(?P<creator_slug>[\w-]+)/$", name="view_creator_references")
    def view_references(self, request, creator_slug=None, category_slug=None, first_filter=None, second_filter=None):
        collections = Collection.objects.select_related("category").filter(hidden=False)
        all_references = Reference.objects.exclude(collections__hidden=True)
        title = self.title
        current = []

        if creator_slug:
            creator = shortcuts.get_object_or_404(Creator, slug=creator_slug)
            all_references = all_references.filter(creators=creator)
            title = creator.get_full_name()

        for slug in (category_slug, first_filter, second_filter):
            if slug:
                collection = shortcuts.get_object_or_404(collections, category__slug=slug)
                current.append(collection.category.slug)
                all_references = all_references.filter(collections=collection)
                title = title + " | " + collection.name

        query = []
        query_string = ""
        order_by = "title"
        order = request.GET.get("order")
        try:
            if order.lstrip("-") in ["title", "date"]:
                order_by = order
                if order.lstrip("-") == "date":
                    secondary = "title"
                else:
                    secondary = "date"
                all_references = all_references.order_by(order_by, secondary)
            query.append("order=" + order)
        except AttributeError:
            pass

        try:
            per_page = abs(int(request.GET.get("results")))
            query.append("results=" + str(per_page))
        except (TypeError, ValueError):
            per_page = 20

        references_page = request.GET.get("page")

        reference_paginator = paginator.Paginator(all_references, per_page)

        if query:
            query_string = "&" + "&".join(query)

        try:
            references = reference_paginator.page(references_page)
        except paginator.PageNotAnInteger:
            # If page is not an integer, deliver first page.
            references = reference_paginator.page(1)
        except paginator.EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            references = reference_paginator.page(references_page.num_pages)

        return self.render(
            request,
            context_overrides={
                "title": title,
                "references": references,
                "collections": collections,
                "current": current,
                "order_by": order_by,
                "creator_slug": creator_slug,
                "query_string": query_string,
            },
        )

    @routable_models.route(r"^(?P<reference_key>[\w-]+)/$")
    def view_reference(self, request, reference_key):
        reference = shortcuts.get_object_or_404(
            Reference.objects.filter(collections__hidden=False).order_by("key").distinct("key"), key=reference_key
        )
        return self.render(
            request,
            context_overrides={
                "reference": reference,
                "collections": Collection.objects.select_related("category").filter(hidden=False),
            },
            template="references/reference.html",
        )
