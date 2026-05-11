from django import forms
from django.core.exceptions import ValidationError
from main.models import Movie, Category


class AddMovieForm(forms.ModelForm):
    """Форма для добавления кинопроекта на основе ModelForm"""
    
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'),
        label='Категория',
        empty_label='Выберите категорию'
    )
    
    class Meta:
        model = Movie
        fields = ['title', 'slug', 'content', 'is_published', 'cat', 'tags', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {
            'title': 'Название фильма',
            'slug': 'URL-идентификатор',
            'content': 'Описание/Синопсис',
            'is_published': 'Опубликовано',
            'cat': 'Категория',
            'tags': 'Теги',
            'photo': 'Постер фильма',
        }
    
    def clean_title(self):
        """Валидация заголовка - бизнес-правило FGM: не более 50 символов"""
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина заголовка не должна превышать 50 символов (бизнес-правило FGM)')
        return title


class UploadFileForm(forms.Form):
    """Форма для загрузки файлов изображений"""
    
    file = forms.ImageField(label='Изображение для проекта')
