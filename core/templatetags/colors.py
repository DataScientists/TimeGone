from django import template
from core.constants import COLORS


register = template.Library()


@register.filter
def color_abbrev(c):
    return COLORS.get(c, "")
