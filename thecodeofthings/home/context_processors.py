import random

from . import models as home_models


def quote(request):
    published_quotes = list(home_models.Quote.objects.filter(is_published=True))
    published_quote = random.choice(published_quotes) if published_quotes else ""
    return {"quote": published_quote}
