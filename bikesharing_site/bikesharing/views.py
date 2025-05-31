import uuid

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from datetime import datetime

from django.views.generic import CreateView, UpdateView, ListView, DetailView

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

class BikeHome(DataMixin, ListView):
    template_name = 'bikesharing/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Bike.published.all().select_related('cat')


@login_required
def about(request):
    contact_list = Bike.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bikesharing/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    template_name = 'bikesharing/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Bike.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'bikesharing/addpage.html'
    title_page = 'Добавление статьи'
    permission_required = 'bikesharing.add_bike'  # <приложение>.<действие>_<таблица>

    def form_valid(self, form):
        b = form.save(commit=False)
        b.author = self.request.user
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


def login(request):
    return HttpResponse("Авторизация")


class BikeCategory(DataMixin, ListView):
    template_name = 'bikesharing/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Bike.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                    title='Категория - ' + cat.name,
                                    cat_selected=cat.pk,
                                    )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(DataMixin, ListView):
    template_name = 'bikesharing/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Bike.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')