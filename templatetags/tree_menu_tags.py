from django import template
from django.urls import reverse
from menu.models import Menu

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path_info
    current_menu = None
    menu_items = Menu.objects.filter(name=menu_name)
    menu_html = '<ul>'

    for menu_item in menu_items:
        if menu_item.url == current_url:
            current_menu = menu_item
        menu_html += '<li><a href="{}"{}>{}</a>'.format(
            menu_item.url,
            ' class="active"' if menu_item.url == current_url else '',
            menu_item.name
        )

        if menu_item.children.all().exists():
            menu_html += '<ul>'
            for child in menu_item.children.all():
                menu_html += '<li><a href="{}"{}>{}</a>'.format(
                    child.url,
                    ' class="active"' if child.url == current_url else '',
                    child.name
                )

                if child.children.all().exists():
                    menu_html += '<ul>'
                    for grandchild in child.children.all():
                        menu_html += '<li><a href="{}"{}>{}</a></li>'.format(
                            grandchild.url,
                            ' class="active"' if grandchild.url == current_url else '',
                            grandchild.name
                        )
                    menu_html += '</ul>'

                menu_html += '</li>'
            menu_html += '</ul>'

        menu_html += '</li>'
    menu_html += '</ul>'

    if current_menu:
        current_menu_ancestors = current_menu.get_ancestors()
        for ancestor in current_menu_ancestors:
            menu_html = menu_html.replace('<a href="{}"'.format(ancestor.url), '<a href="{}" class="expanded"'.format(ancestor.url))
        menu_html = menu_html.replace('<a href="{}"'.format(current_menu.url), '<a href="{}" class="active"'.format(current_menu.url))

    return menu_html