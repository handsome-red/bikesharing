from django import template
from ..models import Bike, Category, TagPost  # Используем относительные импорты

register = template.Library()

@register.inclusion_tag('bikesharing/list_categories.html')
def show_categories(bike_selected=0):
    bikes = Category.objects.all()
    return {"bikes": bikes, 'bike_selected': bike_selected}

@register.inclusion_tag('bikesharing/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.all()}