from django.urls import path, register_converter
from . import views, converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('stations/<int:station_id>/', views.station_detail, name='station'),
    path('stations/<slug:station_slug>/', views.station_by_slug, name='station_slug'),
    path('archive/<year4:year>/', views.archive, name='archive'),
]