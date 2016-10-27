from django import template
from django.template import loader
from django.utils.safestring import mark_safe

from cotidia.account.menu import menu

register = template.Library()


@register.simple_tag(takes_context=True)
def render_menu(context):
    rendered = ""
    for tpl in menu.items():
        t = loader.get_template(tpl)
        rendered += t.render(
            {'perms': context['perms']},
            context['request']
            )
    return mark_safe(rendered)
