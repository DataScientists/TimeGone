from django import template
from core.constants import color2abbr


register = template.Library()


@register.filter
def color_abbrev(c):
    return color2abbr(c)
