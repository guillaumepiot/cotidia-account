from django import template
from django.utils.translation import get_language
from django.template import loader, Context
from django.utils.safestring import mark_safe

register = template.Library()

from account.menu import menu

#
# Return the menu items for the administration panel
#
@register.simple_tag(takes_context=True)
def render_menu(context):
    rendered = ""
    for template in menu.items():
        t = loader.get_template(template)
        c = Context(context)
        rendered += t.render(c)
    return mark_safe(rendered)