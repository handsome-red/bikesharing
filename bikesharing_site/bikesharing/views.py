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
    {
        'id': 1,
        'title': 'Merida Reacto 6000',
        'content': '''
            <h2>Шоссейный велосипед для гонок</h2>
            <p>Лёгкий карбоновый велосипед с аэродинамической рамой. Подходит для профессиональных гонок.</p>

            <h3>Характеристики:</h3>
            <ul>
                <li>Рама: карбон</li>
                <li>Оборудование: Shimano 105</li>
                <li>Вес: 8.3 кг</li>
            </ul>
        ''',
        'is_published': True
    },
    {
        'id': 2,
        'title': 'Merida Big Nine 300',
        'content': '''
            <h2>Горный велосипед</h2>
            <p>Универсальный велосипед для лесных троп и города.</p>

            <h3>Характеристики:</h3>
            <ul>
                <li>Рама: алюминий</li>
                <li>Вилка: SR Suntour</li>
                <li>Вес: 12.8 кг</li>
            </ul>
        ''',
        'is_published': True
    },
    {
        'id': 3,
        'title': 'Merida eSpresso Urban 500',
        'content': '''
            <h2>Городской электровелосипед</h2>
            <p>Комфортный велосипед с электромотором для городских поездок.</p>

            <h3>Характеристики:</h3>
            <ul>
                <li>Двигатель: Yamaha</li>
                <li>Аккумулятор: 500Wh</li>
                <li>Дальность: до 120 км</li>
            </ul>
        ''',
        'is_published': False
    }
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
    return render(request, 'bikesharing/about.html',{'title': 'О сайте', 'menu': menu})

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