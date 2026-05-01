from django import template
from main.models import Category, MovieTag

register = template.Library()


@register.inclusion_tag('main/list_categories.html')
def show_categories(cat_selected_id=0):
    """
    Inclusion tag для отображения списка категорий.
    
    Args:
        cat_selected_id: ID выбранной категории (0 = все категории)
    
    Returns:
        dict: Словарь с категориями и ID выбранной категории
    """
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected_id}


@register.inclusion_tag('main/list_tags.html')
def show_all_tags():
    """
    Inclusion tag для отображения списка всех тегов.
    
    Returns:
        dict: Словарь со всеми тегами
    """
    tags = MovieTag.objects.all()
    return {'tags': tags}
