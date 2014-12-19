from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.tag
def class_active(parser, token):
    try:
        tag_name, x = token.split_contents()
    except ValueError:
        s = "%r tag requires a single argument" % token.contents.split()[0]
        raise template.TemplateSyntaxError(s)
    if not (x[0] == x[-1] and x[0] in ('"', "'")):
        s = "%r tag's argument should be in quotes" % tag_name
        raise template.TemplateSyntaxError(s)
    return ClassActiveNode(x[1:-1])


class ClassActiveNode(template.Node):
    def __init__(self, urlconf_name):
        self.urlconf_name = urlconf_name

    def render(self, context):
        if reverse(self.urlconf_name) == context['path']:
            return 'class="active"'
        else:
            return ''
