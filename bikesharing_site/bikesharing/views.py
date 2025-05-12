from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from datetime import datetime

# Меню вынесено в глобальную переменную (как у вас в примере)
menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content':
        'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content':
        'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content':
        'Биография Джулия Робертс', 'is_published': True},
]

class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'obj': MyClass(10, 20),
        # 'created_at': datetime.now(),  # Раскомментируйте, если нужно добавить дату
    }
    return render(request, 'bikesharing/index.html', context=data)

def about(request):
    return render(request, 'bikesharing/about.html',{'title': 'О сайте'})

def archive(request, year):
    if year > 2023:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Bike Sharing Archive</h1><p>Year: {year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Bike Sharing Page Not Found</h1>')

def addpage(request):
    return HttpResponse("Добавление статьи")

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")

# def station_detail(request, station_id):
#     return HttpResponse(f"<h1>Bike Station Details</h1><p>ID: {station_id}</p>")
#
# def station_by_slug(request, station_slug):
#     if request.GET:
#         print(request.GET)
#     return HttpResponse(f"<h1>Bike Station Details</h1><p>Slug: {station_slug}</p>")