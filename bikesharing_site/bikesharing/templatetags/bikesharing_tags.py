from django import template
import bikesharing.views as views

register = template.Library()

@register.simple_tag(name='getbikes')
def get_categories():
    return views.bike_db

@register.inclusion_tag('bikesharing/list_categories.html')
def show_categories(bike_selected=0):
    bikes = views.bike_db
    return {"bikes": bikes, 'bike_selected': bike_selected}