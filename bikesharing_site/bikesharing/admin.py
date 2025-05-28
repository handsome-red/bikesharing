from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Bike, Category

class ManufacturerPresenceFilter(admin.SimpleListFilter): # необходимо передать ссылку на этот класс в list_filter
    title = 'Наличие производителя'
    parameter_name = 'has_manufacturer' # название параметра

    def lookups(self, request, model_admin): # возвращает значение parameter_name
        return [
            ('yes', 'Есть производитель'), # значение в зависимости от parameter_name
            ('no', 'Нет производителя'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes': # фильтрация по наличию или отсутствию производителя
            return queryset.filter(manufacturer__isnull=False)
        if self.value() == 'no':
            return queryset.filter(manufacturer__isnull=True)
        return queryset

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'slug', 'photo', 'post_photo', 'cat', 'manufacturer', 'tags'] # отображение лишь определенных полей в админ панели
    # exclude = ['tags', 'is_published'] # отображать все поля кроме перечисленных
    readonly_fields = ['post_photo'] # преображение поля в неизменяемый тип
    prepopulated_fields = {"slug": ("title", )}
    #filter_horizontal = ['tags'] # Более удобное отображение таблицы тегов для формирования связи many-to-many
    filter_vertical = ['tags']  # Более удобное отображение таблицы тегов для формирования связи many-to-many
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat') # Отображение полей
    list_display_links = ('title',) # Кликабельность полей
    ordering = ['time_create', 'title'] # Сортировка полей
    list_editable = ('is_published', 'cat') # Добавление функции изменения свойства published через админ панель
    list_per_page = 3 # Значение максимального количества отображения постов на странице
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [ManufacturerPresenceFilter, 'cat__name', 'is_published']
    save_on_top = True

    @admin.display(description="Изображение", ordering='content') # Добавление декоратора для отображения заданного нами имени. а также сортировку по этому полю
    def post_photo(self, bike: Bike):
        if bike.photo:
            return mark_safe(f"<img src='{bike.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Bike.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей") # Отображение сообщение о публикации записей

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Bike.Status.DRAFT)
        self.message_user(request, f"{count} записей снято с публикации", messages.WARNING)  # Отображение сообщение о публикации записей

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') # Отображение полей
    list_display_links = ('id', 'name') # Кликабельность полей

# admin.site.register(Bike, BikeAdmin)