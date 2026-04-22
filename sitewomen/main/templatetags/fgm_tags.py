from django import template

register = template.Library()

@register.inclusion_tag('includes/nav.html')
def show_menu():
    menu = [
        {'title': 'Каталог', 'url_name': 'home'},
        {'title': 'Тарифы', 'url_name': 'home'},
        {'title': 'Источники', 'url_name': 'home'},
        {'title': 'О нас', 'url_name': 'home'},
    ]
    return {'menu': menu}
