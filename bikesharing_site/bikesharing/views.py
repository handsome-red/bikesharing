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
            <h2>Шоссейный аэродинамический велосипед для гонок</h2>
            <p>Merida Reacto 6000 - это высокотехнологичный карбоновый велосипед, созданный для достижения максимальной скорости. Модель 2023 года получила обновлённую аэродинамическую раму CF3, которая на 12% эффективнее предыдущего поколения.</p>

            <h3>Ключевые особенности:</h3>
            <ul>
                <li><strong>Рама</strong>: карбон CF3 с технологией Fast Light (вес 980г)</li>
                <li><strong>Группа оборудования</strong>: Shimano 105 R7100 Di2 (12-скоростная электронная)</li>
                <li><strong>Тормоза</strong>: гидравлические дисковые Shimano 105</li>
                <li><strong>Колёса</strong>: Vision Team 30 Disc (высота обода 30мм)</li>
                <li><strong>Вес</strong>: 8.3 кг в размере M</li>
                <li><strong>Рекомендуемый рост</strong>: 170-185 см</li>
            </ul>

            <h3>Дополнительные характеристики:</h3>
            <p>Велосипед оснащён интегрированным рулём с внутренней прокладкой тросов, что улучшает аэродинамику. Геометрия рамы оптимизирована для агрессивной посадки в стиле "гоночный кокпит". В комплектации идёт с датчиком каденса и компьютером.</p>

            <h3>Идеальное применение:</h3>
            <p>Групповые гонки, триатлон, скоростные покатушки на ровном асфальте. Модель участвовала в UCI World Tour.</p>
        ''',
        'is_published': True
    },
    {
        'id': 2,
        'title': 'Merida Big Nine 300',
        'content': '''
            <h2>Горный хардтейл для кросс-кантри</h2>
            <p>Big Nine 300 - это универсальный алюминиевый хардтейл, который одинаково хорошо показывает себя как на лесных тропах, так и в городских условиях.</p>

            <h3>Технические характеристики:</h3>
            <ul>
                <li><strong>Рама</strong>: алюминий AL-6066 с гидроформовкой</li>
                <li><strong>Вилка</strong>: SR Suntour XCR 32 LO-R (100мм хода, блокировка)</li>
                <li><strong>Передачи</strong>: Shimano Deore 1x10 (11-42T)</li>
                <li><strong>Тормоза</strong>: гидравлические Tektro HD-M275</li>
                <li><strong>Покрышки</strong>: Maxxis Ardent 29x2.25"</li>
                <li><strong>Вес</strong>: 12.8 кг</li>
            </ul>

            <h3>Особенности конструкции:</h3>
            <p>Рама с увеличенным зазором для покрышек до 2.4". Современная слаук-геометрия с длинным верхом и короткой вилкой. Встроенные крепления для багажника и крыльев.</p>

            <h3>Для кого этот велосипед:</h3>
            <p>Начинающие и опытные райдеры, предпочитающие агрессивный стиль катания. Идеален для тренировок и соревнований начального уровня.</p>
        ''',
        'is_published': True
    },
    {
        'id': 3,
        'title': 'Merida eSpresso Urban 500',
        'content': '''
            <h2>Городской электровелосипед премиум-класса</h2>
            <p>eSpresso Urban 500 сочетает в себе современный дизайн и передовые технологии для комфортных городских поездок.</p>

            <h3>Технические параметры:</h3>
            <ul>
                <li><strong>Двигатель</strong>: Yamaha PW-ST (250Вт, 70Нм)</li>
                <li><strong>Аккумулятор</strong>: 500Wh (съёмный, зарядка 4ч)</li>
                <li><strong>Дальность</strong>: 50-120 км в зависимости от режима</li>
                <li><strong>Передачи</strong>: Shimano Nexus 8 (втулка)</li>
                <li><strong>Тормоза</strong>: дисковые гидравлические Tektro</li>
                <li><strong>Дополнительно</strong>: LED-фара, звонок, крылья, багажник</li>
            </ul>

            <h3>Уникальные особенности:</h3>
            <p>Step-through рама для удобной посадки. 5 режимов помощи (включая "турбо"). Встроенный USB-порт для зарядки гаджетов. Мобильное приложение для контроля параметров.</p>

            <h3>Эксплуатация:</h3>
            <p>Идеален для ежедневных поездок на работу, прогулок по городу и за его пределами. Максимальная скорость с ассистентом - 25 км/ч.</p>
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