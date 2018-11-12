from django import template

register = template.Library()


@register.filter
def url_leaf(path):
    parts = path.strip('/').split('/')
    if parts:
        print("return", parts[-1])
        return parts[-1]
    return path
