import random

from . import models as home_models


def william_denton(get_response):
    def middleware(request):
        response = get_response(request)
        published_lines = list(home_models.Line.objects.filter(is_published=True))
        if published_lines:
            response["William-Denton"] = random.choice(published_lines)
        return response

    return middleware
