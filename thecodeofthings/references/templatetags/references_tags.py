import re

from django import template

register = template.Library()


@register.filter
def format_title(value):
    return re.sub(r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))", r" \1", value)
