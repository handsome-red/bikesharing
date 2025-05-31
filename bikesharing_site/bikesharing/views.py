import uuid

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from datetime import datetime

from django.views.generic import CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Bike, Category, TagPost, UploadFiles
from .utils import DataMixin

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
    posts = Bike.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'obj': MyClass(10, 20),
        'bike_selected': 0,
        # 'created_at': datetime.now(),  # Раскомментируйте, если нужно добавить дату
    }
    return render(request, 'bikesharing/index.html', context=data)


# def handle_uploaded_file(f):
#     name = f.name
#     ext = ''
#     if '.' in name:
#         ext = name[name.rindex('.'):]  # Расширение файла
#         name = name[:name.rindex('.')]  # Имя без расширения
#     suffix = str(uuid.uuid4())  # Уникальный суффикс
#     with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

@login_required
def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    return render(request, 'bikesharing/about.html', {
        'title': 'О сайте',
        'menu': menu,
        'form': form
    })

class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'bikesharing/addpage.html'
    title_page = 'Добавление статьи'
    permission_required = 'bikesharing.add_bike'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Bike
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'bikesharing/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'bikesharing.change_bike'

@permission_required(perm='bikesharing.add_bike', raise_exception=True)
def contact(request):
    return HttpResponse("Обратная связь")

def archive(request, year):
    if year > 2023:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Bike Sharing Archive</h1><p>Year: {year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Bike Sharing Page Not Found</h1>')

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                Bike.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
            # form.save()
        return redirect('home')
    else:
        form = AddPostForm()

    return render(request, 'bikesharing/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})



def login(request):
    return HttpResponse("Авторизация")

def show_post(request, post_slug):
    post = get_object_or_404(Bike, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'bikesharing/post.html', context=data)

def show_category(request, bike_slug):
    category = get_object_or_404(Category, slug=bike_slug)
    posts = Bike.published.filter(bike_id=category.pk)

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'obj': MyClass(10, 20),
        'bike_selected': category.pk,
        # 'created_at': datetime.now(),  # Раскомментируйте, если нужно добавить дату
    }
    return render(request, 'bikesharing/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.bikes.filter(is_published=Bike.Status.PUBLISHED)

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'bikesharing/index.html', context=data)

# def station_detail(request, station_id):
#     return HttpResponse(f"<h1>Bike Station Details</h1><p>ID: {station_id}</p>")
#
# def station_by_slug(request, station_slug):
#     if request.GET:
#         print(request.GET)
#     return HttpResponse(f"<h1>Bike Station Details</h1><p>Slug: {station_slug}</p>")