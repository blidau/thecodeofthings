from . import models as blog_models


def sidebar(request):
    recent_posts = blog_models.PostPage.objects.live().public().order_by("-date")[:5]
    categories = blog_models.Category.objects.exclude(postpage__isnull=True)
    blog_page = blog_models.PostIndexPage.objects.live().public().first()
    return {
        "recent_posts": recent_posts,
        "categories": categories,
        "blog_page": blog_page,
    }
