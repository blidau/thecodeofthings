from . import models as blog_models


def sidebar(request):
    about_page = blog_models.StandardPage.objects.live().public().filter(title="About").first()
    recent_posts = blog_models.PostPage.objects.live().public().order_by("-date")[:5]
    categories = blog_models.Category.objects.exclude(postpage__isnull=True)
    blog_page = blog_models.PostIndexPage.objects.live().public().first()
    return {
        "about_page": about_page,
        "recent_posts": recent_posts,
        "categories": categories,
        "blog_page": blog_page,
    }
