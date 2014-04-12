from django import template

register = template.Library()

@register.simple_tag
def see_url(title):
    """ Returns a wiki URL from an article title """

    return title
