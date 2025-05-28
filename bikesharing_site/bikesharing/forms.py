from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Manufacturer, Bike


@deconstructible
class RussianValidator:
    ALLOWED_CHARS ="АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'
    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})

class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), required=False, empty_label="Производителя нет", label="Производитель")

    class Meta:
        model = Bike
        # fields = '__all__' # Позволяет отобразить все поля, кроме тех, что отображаются автоматически
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'manufacturer', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60,
            'rows': 10}),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")  # Для произвольных файлов
    # file = forms.ImageField(label="Изображение") # Для изображений