from django import template
from main.models import Category

register = template.Library()

@register.inclusion_tag('includes/nav.html')
def show_menu():
    menu = [
        {'title': 'Каталог', 'url_name': 'home'},
        {'title': 'Источники', 'url_name': 'sources'},
        {'title': 'О нас', 'url_name': 'about'},
        {'title': 'Контакты', 'url_name': 'contact'},
        {'title': 'ИИ', 'url_name': 'ai_assistant'},
    ]
    return {'menu': menu}

@register.inclusion_tag('includes/categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}
