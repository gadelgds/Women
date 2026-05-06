# FGM (Film & Game Management) - Документация проекта

## Обзор проекта

**FGM** - это веб-приложение для управления кинопроизводством, построенное на Django 5.2.8. Проект представляет собой платформу для координации рабочих процессов в киноиндустрии, объединяющую производственные данные на одной облачной платформе.

### Основная информация
- **Название:** sitewomen (техническое), FGM (бизнес)
- **Фреймворк:** Django 5.2.8
- **База данных:** SQLite3
- **Python версия:** 3.12.0
- **Язык интерфейса:** Русский
- **Статус:** В разработке

---

## Архитектура проекта

### Структура директорий

```
django/
├── djvenv/                          # Виртуальное окружение Python
├── sitewomen/                       # Корневая директория проекта
│   ├── sitewomen/                   # Конфигурация Django проекта
│   │   ├── settings.py              # Настройки проекта
│   │   ├── urls.py                  # Главный URL-роутер
│   │   ├── wsgi.py                  # WSGI конфигурация
│   │   └── asgi.py                  # ASGI конфигурация
│   ├── main/                        # Основное приложение
│   │   ├── models.py                # Модели данных
│   │   ├── views.py                 # Представления (контроллеры)
│   │   ├── urls.py                  # URL-маршруты приложения
│   │   ├── admin.py                 # Конфигурация админ-панели
│   │   ├── converters.py            # Кастомные URL-конвертеры
│   │   ├── templates/               # HTML-шаблоны
│   │   ├── static/                  # Статические файлы (CSS, JS, изображения)
│   │   ├── templatetags/            # Кастомные теги шаблонов
│   │   ├── management/commands/     # Кастомные Django команды
│   │   └── migrations/              # Миграции базы данных
│   ├── db.sqlite3                   # База данных SQLite
│   └── manage.py                    # Django CLI утилита
```

---

## Модели данных (models.py)

### 1. Category (Категория)

Модель для категоризации фильмов.

**Поля:**
- `id` - BigAutoField (автоматический первичный ключ)
- `name` - CharField(max_length=100) - Название категории
- `slug` - SlugField(max_length=255, unique=True) - URL-идентификатор

**Методы:**
- `__str__()` - Возвращает название категории
- `get_absolute_url()` - Генерирует URL: `/category/<slug>/`

**Meta:**
- `verbose_name` = "Категория"
- `verbose_name_plural` = "Категории"
- `ordering` = ['name'] - Сортировка по алфавиту

**Связи:**
- Обратная связь с Movie через `related_name='movies'`

---

### 2. MovieTag (Тег фильма)

**НОВАЯ МОДЕЛЬ** - Добавлена для системы тегов.

Модель для тегирования фильмов (ManyToMany связь).

**Поля:**
- `id` - BigAutoField (автоматический первичный ключ)
- `tag` - CharField(max_length=100) - Название тега
- `slug` - SlugField(max_length=255, unique=True) - URL-идентификатор

**Методы:**
- `__str__()` - Возвращает название тега
- `get_absolute_url()` - Генерирует URL: `/tag/<slug>/`

**Meta:**
- `verbose_name` = "Тег"
- `verbose_name_plural` = "Теги"
- `ordering` = ['tag'] - Сортировка по алфавиту

**Связи:**
- Обратная связь с Movie через `related_name='movies'`
- ManyToMany связь (один тег - много фильмов, один фильм - много тегов)

---

### 3. TechnicalSpecs (Технический паспорт)

**НОВАЯ МОДЕЛЬ** - Добавлена для хранения технических характеристик фильма.

Модель для технических спецификаций фильма (OneToOne связь).

**Поля:**
- `id` - BigAutoField (автоматический первичный ключ)
- `movie` - OneToOneField(Movie, on_delete=CASCADE) - Связь с фильмом
- `resolution` - CharField(max_length=50, default="4K") - Разрешение
- `camera` - CharField(max_length=100) - Камера
- `color_space` - CharField(max_length=50) - Цветовое пространство

**Методы:**
- `__str__()` - Возвращает строку "Техпаспорт для {название фильма}"

**Meta:**
- `verbose_name` = "Технический паспорт"
- `verbose_name_plural` = "Технические паспорта"

**Связи:**
- OneToOne связь с Movie через `related_name='specs'`
- При удалении фильма техпаспорт удаляется автоматически (CASCADE)

**Почему CASCADE:**
- Техпаспорт не может существовать без фильма (зависимая сущность)
- Автоматическая очистка при удалении фильма
- Предотвращает "осиротевшие" записи в БД
- Стандартная практика для OneToOne с зависимыми данными

---

### 4. Movie (Фильм/Кинопроект)

Основная модель для хранения информации о кинопроектах.

**Поля:**
- `id` - BigAutoField (автоматический первичный ключ)
- `title` - CharField(max_length=255) - Название фильма
- `slug` - SlugField(max_length=255, unique=True) - URL-идентификатор
- `content` - TextField(blank=True) - Описание/синопсис
- `time_create` - DateTimeField(auto_now_add=True) - Дата создания
- `time_update` - DateTimeField(auto_now=True) - Дата обновления
- `is_published` - BooleanField - Статус публикации (0=Черновик, 1=Опубликовано)
- `cat` - ForeignKey(Category, on_delete=PROTECT) - Связь с категорией
- `tags` - ManyToManyField(MovieTag, blank=True) - **НОВОЕ ПОЛЕ** - Теги фильма

**Вложенный класс Status:**
```python
class Status(models.IntegerChoices):
    DRAFT = 0, 'Черновик'
    PUBLISHED = 1, 'Опубликовано'
```

**Менеджеры:**

1. `objects` - Стандартный менеджер Django (все записи)
2. `published` - Кастомный менеджер (только опубликованные)

**Кастомный менеджер PublishedManager:**
```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Movie.Status.PUBLISHED)
```

**Методы:**
- `__str__()` - Возвращает название фильма
- `get_absolute_url()` - Генерирует URL: `/movie/<slug>/`

**Meta:**
- `verbose_name` = "Кинопроект"
- `verbose_name_plural` = "Кинопроекты"
- `ordering` = ['-time_create'] - Сортировка по дате (новые первыми)
- `indexes` = [Index(fields=['-time_create'])] - Индекс для оптимизации

**Связи:**
- ForeignKey к Category с защитой `on_delete=models.PROTECT`
- При попытке удалить категорию с фильмами выбрасывается ProtectedError

---

## URL-маршруты

### Главный роутер (sitewomen/urls.py)

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
handler404 = 'main.views.page_not_found'
```

### Маршруты приложения (main/urls.py)

| URL | View | Name | Описание |
|-----|------|------|----------|
| `/основа/` | index | home | Главная страница со всеми фильмами |
| `/о-нас/` | about | about | Страница "О нас" |
| `/источники/` | sources | sources | Страница источников |
| `/movie/<slug>/` | show_movie | movie_detail | Детальная страница фильма |
| `/category/<slug>/` | show_category | category | Фильмы по категории |
| `/tag/<slug>/` | show_tag_postlist | tag | **НОВЫЙ** - Фильмы по тегу |
| `/cats/<int>/` | categories | cats_id | Категории по ID (legacy) |
| `/cats/<slug>/` | categories_by_slug | cats_slug | Категории по slug (legacy) |
| `/archive/<year4>/` | archive | archive_year | Архив по годам |
| `/login/` | login | login | Страница входа |

**Кастомный конвертер year4:**
```python
class FourDigitYearConverter:
    regex = "[0-9]{4}"
    def to_python(self, value): return int(value)
    def to_url(self, value): return "%04d" % value
```

---

## Представления (Views)

### 1. index(request)
**URL:** `/основа/`  
**Назначение:** Главная страница с каталогом всех опубликованных фильмов

**Логика:**
```python
posts = Movie.published.all()  # Только опубликованные
```

**Контекст:**
- `title` - "FGM — Управление кинопроизводством"
- `posts` - QuerySet опубликованных фильмов
- `cat_selected` - 0 (для подсветки "Все категории")

---

### 2. show_movie(request, movie_slug)
**URL:** `/movie/<slug>/`  
**Назначение:** Детальная страница конкретного фильма

**Логика:**
```python
movie = get_object_or_404(Movie, slug=movie_slug)
```

**Контекст:**
- `title` - Название фильма
- `movie` - Объект Movie

**Обработка ошибок:** 404 если фильм не найден

---

### 3. show_category(request, cat_slug)
**URL:** `/category/<slug>/`  
**Назначение:** Фильмы конкретной категории

**Логика:**
```python
category = get_object_or_404(Category, slug=cat_slug)
posts = Movie.published.filter(cat_id=category.pk)
```

**Контекст:**
- `title` - Название категории
- `posts` - Отфильтрованные фильмы
- `cat_selected` - ID категории (для подсветки в меню)

**Особенности:**
- Использует тот же шаблон что и главная (index.html)
- Двойная фильтрация: по статусу публикации И по категории

---

### 4. show_tag_postlist(request, tag_slug) **НОВЫЙ**
**URL:** `/tag/<slug>/`  
**Назначение:** Фильмы с конкретным тегом

**Логика:**
```python
tag = get_object_or_404(MovieTag, slug=tag_slug)
posts = tag.movies.filter(is_published=Movie.Status.PUBLISHED)
```

**Контекст:**
- `title` - Название тега
- `posts` - Фильмы с этим тегом
- `cat_selected` - None (теги не связаны с категориями)

**Особенности:**
- Использует ManyToMany связь через `tag.movies`
- Фильтрует только опубликованные фильмы
- Использует тот же шаблон index.html

---

### 5. about(request)
**URL:** `/о-нас/`  
**Назначение:** Информация о проекте

---

### 6. sources(request)
**URL:** `/источники/`  
**Назначение:** Список источников и ссылок

---

### 6. page_not_found(request, exception)
**Назначение:** Обработчик 404 ошибок

---

## Шаблоны (Templates)

### Структура шаблонов

```
templates/
├── base.html                    # Базовый шаблон
├── includes/
│   ├── header.html             # Шапка сайта
│   └── nav.html                # Навигационное меню
└── main/
    ├── index.html              # Главная/каталог
    ├── movie_detail.html       # Детальная страница фильма
    ├── about.html              # О нас
    └── sources.html            # Источники
```

### base.html - Базовый шаблон

**Структура:**
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <title>{{ title|capfirst }}</title>
    <!-- CSS файлы -->
</head>
<body>
    <div class="screen">
        {% include 'includes/header.html' %}
        {% block content %}{% endblock %}
        <footer>...</footer>
    </div>
</body>
</html>
```

**Подключаемые стили:**
- `globals.css` - Глобальные стили
- `styleguide.css` - Руководство по стилю
- `style.css` - Основные стили

---

### index.html - Главная страница

**Секции:**
1. **Hero Section** - Приветственный блок с формой подписки
2. **Main Content** - Список фильмов
3. **Features Section** - Преимущества платформы
4. **Trust Section** - Почему нам доверяют
5. **Product Section** - Информация о продукте
6. **CTA Section** - Призыв к действию

**Вывод фильмов:**
```django
{% for p in posts %}
  {% if p.is_published %}
  <article class="post-item">
    <p class="category-badge">Категория: {{ p.cat.name }}</p>
    <p class="movie-updated">Обновлено: {{ p.time_update|date:"d-m-Y H:i:s" }}</p>
    <h2>{{ p.title }}</h2>
    {% with p.tags.all as tags %}
      {% if tags %}
      <p class="movie-tags">
        Теги: 
        {% for tag in tags %}
          <a href="{{ tag.get_absolute_url }}">#{{ tag.tag }}</a>
        {% endfor %}
      </p>
      {% endif %}
    {% endwith %}
    <p>{{ p.content|truncatewords:30 }}</p>
    <p>Категория: <a href="{{ p.cat.get_absolute_url }}">{{ p.cat.name }}</a></p>
    <a href="{{ p.get_absolute_url }}">Читать далее →</a>
  </article>
  {% endif %}
{% endfor %}
```

**Обновления:**
- ✅ Добавлена дата обновления с форматированием `d-m-Y H:i:s`
- ✅ Добавлен вывод тегов под заголовком
- ✅ Использована оптимизация `{% with p.tags.all as tags %}`

---

### movie_detail.html - Детальная страница

**Отображаемая информация:**
- Название фильма
- **НОВОЕ:** Теги фильма (под заголовком)
- Дата создания (форматированная)
- Дата обновления
- Полное описание
- Кнопка возврата к списку

**Вывод тегов:**
```django
<h1>{{ movie.title }}</h1>
{% with movie.tags.all as tags %}
  {% if tags %}
  <p class="movie-tags">
    Теги: 
    {% for tag in tags %}
      <a href="{{ tag.get_absolute_url }}">#{{ tag.tag }}</a>
    {% endfor %}
  </p>
  {% endif %}
{% endwith %}
```

---

## Кастомные теги шаблонов

### main_tags.py (ОБНОВЛЕН)

**Тег show_categories:**
```python
@register.inclusion_tag('main/list_categories.html')
def show_categories(cat_selected_id=0):
    """Отображение списка категорий с подсветкой активной"""
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected_id}
```

**Использование:**
```django
{% load main_tags %}
{% show_categories cat_selected %}
```

**Тег show_all_tags (НОВЫЙ):**
```python
@register.inclusion_tag('main/list_tags.html')
def show_all_tags():
    """Отображение списка всех тегов"""
    tags = MovieTag.objects.all()
    return {'tags': tags}
```

**Использование:**
```django
{% load main_tags %}
{% show_all_tags %}
```

---

### fgm_tags.py (LEGACY)

**Тег show_menu:**
```python
@register.inclusion_tag('includes/nav.html')
def show_menu():
    menu = [
        {'title': 'Каталог', 'url_name': 'home'},
        {'title': 'Тарифы', 'url_name': 'home'},
        {'title': 'Источники', 'url_name': 'sources'},
        {'title': 'О нас', 'url_name': 'about'},
    ]
    return {'menu': menu}
```

**Использование:**
```django
{% load fgm_tags %}
{% show_menu %}
```

---

## Административная панель (Admin)

### MovieAdmin

**Конфигурация:**
```python
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'time_update', 'is_published')
    list_filter = ('is_published', 'time_create')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    ordering = ('-time_create',)
```

**Возможности:**
- Просмотр списка фильмов с ключевыми полями
- Фильтрация по статусу публикации и дате
- Поиск по названию и содержимому
- Быстрое изменение статуса публикации
- Сортировка по дате создания

---

## Management команды

### add_movies.py

**Команда:** `python manage.py add_movies`

**Назначение:** Добавление тестовых данных в БД

**Создаваемые фильмы:**
1. Марсианская одиссея
2. Код вечности
3. Тайны спецэффектов

**Использование:**
```bash
python manage.py add_movies
```

---

## Миграции базы данных

### История миграций

| Миграция | Описание |
|----------|----------|
| 0001_initial.py | Создание модели Movie |
| 0002_auto_20260425_2242.py | Автоматические изменения |
| 0003_remove_movie_main_movie_time_cr_idx.py | Удаление старого индекса |
| 0004_movie_slug_movie_main_movie_time_cr_21bfb2_idx.py | Добавление slug и индекса |
| 0005_alter_movie_slug.py | Изменение поля slug |
| 0006_alter_movie_is_published.py | Изменение поля is_published |
| 0007_category_alter_movie_slug_movie_cat.py | Добавление Category и связи |
| 0008_alter_movie_cat.py | Удаление null=True из cat |

---

## Настройки проекта (settings.py)

### Основные настройки

```python
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']
SECRET_KEY = 'django-insecure-...'
```

### Установленные приложения

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',      # Расширения Django
    'main.apps.MainConfig',   # Основное приложение
]
```

### База данных

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Интернационализация

```python
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
```

### Статические файлы

```python
STATIC_URL = 'static/'
```

---

## Механизм фильтрации

### Главная страница

**SQL-запрос:**
```sql
SELECT * FROM main_movie 
WHERE is_published = 1 
ORDER BY time_create DESC;
```

**Результат:** Все опубликованные фильмы

---

### Страница категории

**SQL-запрос:**
```sql
SELECT * FROM main_movie 
WHERE is_published = 1 AND cat_id = <category_id>
ORDER BY time_create DESC;
```

**Результат:** Опубликованные фильмы конкретной категории

---

## Защита данных (on_delete=PROTECT)

### Механизм работы

При попытке удалить категорию с привязанными фильмами:

1. Django выполняет SELECT для поиска зависимостей
2. Если найдены связанные фильмы → выбрасывается `ProtectedError`
3. DELETE не выполняется, данные остаются в безопасности

**Пример:**
```python
category.delete()
# ProtectedError: Cannot delete some instances of model 'Category' 
# because they are referenced through protected foreign keys: 'Movie.cat'.
```

---

## Статические файлы

### Структура

```
static/main/
├── css/
│   ├── globals.css      # Глобальные стили
│   ├── styleguide.css   # Руководство по стилю
│   └── style.css        # Основные стили
└── img/
    ├── Logo.svg
    ├── vector.svg
    ├── image-*.png
    └── social icons (whatsapp, vk, mail)
```

---

## Особенности реализации

### 1. Кастомный менеджер published

**Преимущества:**
- Автоматическая фильтрация по статусу
- Не нужно везде писать `.filter(is_published=1)`
- Единая точка контроля логики публикации

**Использование:**
```python
Movie.published.all()           # Только опубликованные
Movie.published.filter(cat=c)   # Опубликованные + фильтр
Movie.objects.all()             # Все записи
```

---

### 2. SEO-дружественные URL

**Slug вместо ID:**
- `/movie/marsinskaya-odisseya/` вместо `/movie/1/`
- `/category/sci-fi/` вместо `/category/1/`

**Преимущества:**
- Понятные URL для пользователей
- Лучше для SEO
- Уникальность гарантирована (unique=True)

---

### 3. Переиспользование шаблонов

**index.html используется для:**
- Главной страницы (все фильмы)
- Страниц категорий (фильтрованные фильмы)

**Преимущества:**
- Единообразный дизайн
- Легче поддерживать
- Меньше дублирования кода

---

### 4. Inclusion tags

**show_menu** генерирует навигацию динамически:
- Централизованное управление меню
- Легко добавлять/удалять пункты
- Переиспользуется в header и footer

---

## Workflow разработки

### 1. Создание модели
```bash
# Редактируем models.py
python manage.py makemigrations
python manage.py migrate
```

### 2. Регистрация в админке
```python
# admin.py
@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    ...
```

### 3. Создание представления
```python
# views.py
def view_name(request):
    data = Model.objects.all()
    return render(request, 'template.html', {'data': data})
```

### 4. Настройка URL
```python
# urls.py
path('url/', views.view_name, name='name'),
```

### 5. Создание шаблона
```django
{% extends 'base.html' %}
{% block content %}
    <!-- Контент -->
{% endblock %}
```

---

## Запуск проекта

### Активация виртуального окружения
```bash
# Windows
djvenv\Scripts\activate

# Linux/Mac
source djvenv/bin/activate
```

### Запуск сервера разработки
```bash
cd sitewomen
python manage.py runserver
```

### Доступ к приложению
- **Сайт:** http://127.0.0.1:8000/основа/
- **Админка:** http://127.0.0.1:8000/admin/

### Полезные команды
```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Shell с автозагрузкой моделей
python manage.py shell_plus

# Shell с выводом SQL
python manage.py shell_plus --print-sql

# Добавление тестовых данных
python manage.py add_movies
```

---

## Безопасность

### Текущие настройки (Development)
- `DEBUG = True` - Включен режим отладки
- `SECRET_KEY` - Хранится в коде (небезопасно для production)
- `ALLOWED_HOSTS = ['127.0.0.1']` - Только локальный доступ

### Рекомендации для Production
1. Установить `DEBUG = False`
2. Вынести `SECRET_KEY` в переменные окружения
3. Настроить `ALLOWED_HOSTS` для реального домена
4. Использовать PostgreSQL вместо SQLite
5. Настроить HTTPS
6. Включить CSRF защиту
7. Настроить статические файлы через CDN

---

## Зависимости

### Основные пакеты
- Django 5.2.8
- django-extensions (для shell_plus и других утилит)

### Установка зависимостей
```bash
pip install django==5.2.8
pip install django-extensions
```

---

## Будущие улучшения

### Функциональность
- [ ] Система аутентификации пользователей
- [ ] Комментарии к фильмам
- [ ] Рейтинги и отзывы
- [ ] Поиск по фильмам
- [ ] Пагинация списков
- [ ] Фильтры (по году, жанру, статусу)
- [ ] API для мобильных приложений
- [ ] Уведомления о новых фильмах

### Технические улучшения
- [ ] Миграция на PostgreSQL
- [ ] Кэширование (Redis)
- [ ] Celery для фоновых задач
- [ ] Docker контейнеризация
- [ ] CI/CD pipeline
- [ ] Автоматические тесты
- [ ] Логирование
- [ ] Мониторинг производительности

---

## Контакты и поддержка

**Автор:** Губайдуллин  
**Год:** 2025  
**Лицензия:** Все права защищены

---

## Заключение

FGM - это современное Django-приложение для управления кинопроизводством с чистой архитектурой, использующее лучшие практики разработки:

✅ Модульная структура  
✅ Кастомные менеджеры для бизнес-логики  
✅ SEO-оптимизированные URL  
✅ Защита данных через PROTECT  
✅ Переиспользуемые компоненты  
✅ Административная панель  
✅ Расширяемая архитектура

Проект готов к дальнейшему развитию и масштабированию.


---

## История изменений и обновлений

### Версия 2.0 - Система категорий и тегов (Май 2026)

#### Добавлена модель MovieTag
- Новая модель для тегирования фильмов
- ManyToMany связь с Movie
- Поля: tag, slug
- Метод get_absolute_url()

#### Обновлена модель Movie
- Добавлено поле `tags` (ManyToManyField)
- Обновлено поле `cat` (теперь обязательное, без null=True)
- Добавлен параметр `cat_selected` в контекст views

#### Новые URL-маршруты
- `/category/<slug>/` - фильтрация по категориям
- `/tag/<slug>/` - фильтрация по тегам

#### Новые представления (Views)
- `show_category()` - отображение фильмов категории
- `show_tag_postlist()` - отображение фильмов по тегу

#### Система навигации
- Динамическое меню категорий из БД
- Динамическое меню тегов из БД
- Подсветка активной категории
- Inclusion tags: `show_categories()`, `show_all_tags()`

#### Обновления шаблонов
- `base.html` - добавлены меню категорий и тегов
- `index.html` - добавлены теги под заголовком, дата обновления
- `movie_detail.html` - добавлены теги под заголовком
- `list_categories.html` - новый шаблон для меню категорий
- `list_tags.html` - новый шаблон для меню тегов

#### Оптимизация
- Использование `{% with %}` для кэширования запросов тегов
- Кастомный менеджер `published` для фильтрации
- Индексы на полях для быстрого поиска

---

## Миграции базы данных (обновлено)

### История миграций

| Миграция | Описание |
|----------|----------|
| 0001_initial.py | Создание модели Movie |
| 0002_auto_20260425_2242.py | Автоматические изменения |
| 0003_remove_movie_main_movie_time_cr_idx.py | Удаление старого индекса |
| 0004_movie_slug_movie_main_movie_time_cr_21bfb2_idx.py | Добавление slug и индекса |
| 0005_alter_movie_slug.py | Изменение поля slug |
| 0006_alter_movie_is_published.py | Изменение поля is_published |
| 0007_category_alter_movie_slug_movie_cat.py | Добавление Category и связи |
| 0008_alter_movie_cat.py | Удаление null=True из cat |
| 0009_movietag_movie_tags.py | Добавление MovieTag и поля tags |
| **0010_technicalspecs.py** | **НОВАЯ** - Добавление TechnicalSpecs (OneToOne) |

### Структура БД после миграций

**Таблицы:**
1. `main_movie` - основная таблица фильмов
2. `main_category` - таблица категорий
3. `main_movietag` - таблица тегов
4. `main_movie_tags` - промежуточная таблица для ManyToMany
5. `main_technicalspecs` - таблица технических паспортов

**Связи:**
- Movie → Category (ForeignKey, PROTECT)
- Movie ←→ MovieTag (ManyToMany через main_movie_tags)
- Movie ← TechnicalSpecs (OneToOne, CASCADE)

---

## Работа с данными

### Создание категорий

```python
from main.models import Category

cat = Category.objects.create(
    name="Sci-Fi",
    slug="sci-fi"
)
```

### Создание тегов

```python
from main.models import MovieTag

tag = MovieTag.objects.create(
    tag="Action",
    slug="action"
)
```

### Привязка тегов к фильму

```python
from main.models import Movie

movie = Movie.objects.first()

# Добавить теги
movie.tags.add(tag1, tag2, tag3)

# Установить теги (заменяет существующие)
movie.tags.set([tag1, tag2])

# Удалить тег
movie.tags.remove(tag1)

# Очистить все теги
movie.tags.clear()
```

### Получение данных

```python
# Все теги фильма
tags = movie.tags.all()

# Все фильмы с тегом
movies = tag.movies.filter(is_published=Movie.Status.PUBLISHED)

# Фильмы категории
movies = category.movies.filter(is_published=Movie.Status.PUBLISHED)
```

---

## Особенности реализации

### 1. Защита данных (on_delete=PROTECT)

При попытке удалить категорию с привязанными фильмами:
- Django выполняет SELECT для поиска зависимостей
- Выбрасывается `ProtectedError`
- DELETE не выполняется
- Данные остаются в безопасности

### 2. Кастомный менеджер published

Автоматическая фильтрация опубликованных фильмов:
```python
Movie.published.all()  # Только опубликованные
Movie.objects.all()    # Все записи
```

### 3. ManyToMany связь для тегов

Гибкая связь:
- Один фильм может иметь много тегов
- Один тег может быть у многих фильмов
- Автоматическая промежуточная таблица
- Удобные методы: add(), remove(), clear(), set()

### 4. Оптимизация запросов

Использование `{% with %}` в шаблонах:
```django
{% with movie.tags.all as tags %}
  <!-- Один запрос вместо нескольких -->
{% endwith %}
```

### 5. Динамические меню

Inclusion tags загружают данные из БД:
- Автоматическое обновление при добавлении категорий/тегов
- Не требуется изменение кода
- Централизованное управление

---

## Рекомендации по использованию

### Для разработчиков

1. **Всегда используйте кастомный менеджер `published`** для отображения фильмов пользователям
2. **Используйте `{% with %}`** при работе с ManyToMany полями в шаблонах
3. **Создавайте миграции** после каждого изменения моделей
4. **Тестируйте защиту PROTECT** перед удалением категорий

### Для контент-менеджеров

1. **Всегда указывайте категорию** при создании фильма (обязательное поле)
2. **Добавляйте теги** для улучшения навигации и поиска
3. **Используйте уникальные slug** для категорий и тегов
4. **Проверяйте связи** перед удалением категорий

---

## Будущие улучшения

### Планируемые функции

- [ ] Счетчик фильмов в категориях и тегах
- [ ] Облако тегов с размером по популярности
- [ ] Похожие фильмы на основе тегов
- [ ] Фильтрация по нескольким тегам одновременно
- [ ] Автоматическое создание slug из названия
- [ ] Кэширование меню категорий и тегов
- [ ] Пагинация списков фильмов
- [ ] Поиск по названию, описанию и тегам
- [ ] Сортировка фильмов (по дате, названию, популярности)
- [ ] Экспорт списка фильмов в CSV/Excel

### Технические улучшения

- [ ] Миграция на PostgreSQL
- [ ] Полнотекстовый поиск
- [ ] Кэширование через Redis
- [ ] API для мобильных приложений
- [ ] Автоматические тесты
- [ ] CI/CD pipeline
- [ ] Docker контейнеризация

---

## Заключение

FGM - это современное Django-приложение для управления кинопроизводством с развитой системой категоризации и тегирования. Проект использует лучшие практики Django:

✅ **Модульная архитектура** - четкое разделение моделей, представлений и шаблонов  
✅ **Кастомные менеджеры** - инкапсуляция бизнес-логики  
✅ **Защита данных** - PROTECT для критичных связей  
✅ **ManyToMany связи** - гибкая система тегирования  
✅ **Динамические меню** - автоматическое обновление из БД  
✅ **Оптимизация запросов** - использование {% with %} и select_related  
✅ **SEO-оптимизация** - понятные URL и семантическая разметка  
✅ **Переиспользование кода** - DRY принцип  

Проект готов к дальнейшему развитию и масштабированию! 🎬
---

### Версия 2.1 - Настройка административной панели (Май 2026)

#### Локализация интерфейса
- `LANGUAGE_CODE = "ru-RU"` в settings.py
- Все модели имеют `verbose_name` и `verbose_name_plural` на русском языке

#### Глобальные заголовки админ-панели (urls.py)
```python
admin.site.site_header = "FGM: Система управления кинопроизводством"
admin.site.index_title = "Панель продюсера и инженера"
```

#### Настройка приложения (apps.py)
```python
class MainConfig(AppConfig):
    verbose_name = "Управление контентом"
```

#### Django Debug Toolbar
- Добавлен `"debug_toolbar"` в INSTALLED_APPS
- `DebugToolbarMiddleware` добавлен сразу после `SessionMiddleware`
- `INTERNAL_IPS = ["127.0.0.1"]`
- URL `__debug__/` подключается при `settings.DEBUG`

#### CategoryAdmin - расширенная конфигурация
```python
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    prepopulated_fields = dict(slug=["name"])
    search_fields = ("name",)
```

#### MovieTagAdmin
```python
@admin.register(MovieTag)
class MovieTagAdmin(admin.ModelAdmin):
    list_display = ("tag", "slug")
    prepopulated_fields = dict(slug=["tag"])
    search_fields = ("tag",)
```

#### TechnicalSpecsInline
- StackedInline для редактирования техпаспорта на странице фильма
- `extra = 0` - не показывать пустые формы

#### TechnicalSpecsFilter - кастомный фильтр
```python
class TechnicalSpecsFilter(admin.SimpleListFilter):
    title = "Наличие техпаспорта"
    parameter_name = "tech_status"
    
    def lookups(self, request, model_admin):
        return [("filled", "Заполнен"), ("empty", "Пусто")]
    
    def queryset(self, request, queryset):
        if self.value() == "filled":
            return queryset.filter(specs__isnull=False)
        if self.value() == "empty":
            return queryset.filter(specs__isnull=True)
```

#### MovieAdmin - полная конфигурация
```python
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # Отображение в списке
    list_display = ("title", "cat", "brief_info", "time_create", "is_published")
    list_display_links = ("title",)
    list_editable = ("is_published", "cat")
    
    # Поиск и фильтрация
    search_fields = ("title__startswith", "cat__name")
    list_filter = (TechnicalSpecsFilter, "is_published", "cat", "time_create")
    
    # Форма редактирования
    fields = ("title", "slug", "cat", "content", "tags")
    prepopulated_fields = dict(slug=["title"])
    filter_horizontal = ("tags",)
    
    # Inline и пагинация
    inlines = [TechnicalSpecsInline]
    ordering = ["-time_create", "title"]
    list_per_page = 10
    
    # Аналитическое поле
    @admin.display(description="Объем описания")
    def brief_info(self, obj):
        return f"Описание: {len(obj.content)} симв."
    
    # Массовые действия
    @admin.action(description="Опубликовать выбранные фильмы")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Movie.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} записей.")
    
    @admin.action(description="Снять с публикации выбранные проекты")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Movie.Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} записей.", level=messages.WARNING)
    
    actions = ["set_published", "set_draft"]
```

#### TechnicalSpecsAdmin
```python
@admin.register(TechnicalSpecs)
class TechnicalSpecsAdmin(admin.ModelAdmin):
    list_display = ("movie", "resolution", "camera", "color_space")
    search_fields = ("movie__title", "camera")
    list_filter = ("resolution",)
```

#### Ключевые возможности админ-панели

| Функция | Описание |
|---------|----------|
| Поиск по названию | `title__startswith` - поиск по началу строки |
| Поиск по категории | `cat__name` - поиск по связанному полю |
| Фильтр по техпаспорту | Кастомный TechnicalSpecsFilter |
| Горизонтальный селектор тегов | `filter_horizontal` для ManyToMany |
| Автозаполнение slug | Из поля title |
| Массовая публикация | Action `set_published` |
| Массовое снятие | Action `set_draft` с warning |
| Аналитика описания | Поле `brief_info` с длиной текста |
| Inline техпаспорт | Редактирование на странице фильма |

#### Измененные файлы

| Файл | Изменения |
|------|-----------|
| `sitewomen/settings.py` | LANGUAGE_CODE, debug_toolbar, INTERNAL_IPS |
| `sitewomen/urls.py` | Глобальные заголовки, маршрут debug_toolbar |
| `main/apps.py` | verbose_name приложения |
| `main/admin.py` | Полная переработка всех Admin классов |


#### Кастомизация внешнего вида админки

**Структура файлов:**
```
sitewomen/
├── templates/
│   └── admin/
│       └── base_site.html    # Кастомный шаблон админки
└── static/
    └── css/
        └── admin/
            └── admin.css     # Фирменные стили
```

**templates/admin/base_site.html:**
```django
{% extends "admin/base.html" %}
{% load static %}

{% block title %}FGM | Панель управления{% endblock %}

{% block branding %}
<h1 id="site-name">FGM Production Hub</h1>
{% endblock %}

{% block extrastyle %}
<link rel="stylesheet" href="{% static 'css/admin/admin.css' %}">
{% endblock %}
```

**static/css/admin/admin.css:**
```css
/* FGM Admin Color Scheme */

#header {
    background-color: #3F4137;  /* Темно-оливковый */
}

.module h2,
.module caption {
    background-color: #3F4137;
}

div.breadcrumbs {
    background-color: #6A6E5D;  /* Серый */
}
```

**Обновления settings.py:**
```python
TEMPLATES = [
    {
        "DIRS": [BASE_DIR / "templates"],  # Путь к кастомным шаблонам
        ...
    },
]

STATICFILES_DIRS = [BASE_DIR / "static"]  # Путь к кастомным стилям
```

**Фирменная палитра:**
| Элемент | Цвет | HEX |
|---------|------|-----|
| Шапка (#header) | Темно-оливковый | #3F4137 |
| Заголовки блоков | Темно-оливковый | #3F4137 |
| Хлебные крошки | Серый | #6A6E5D |

**Новые файлы:**
| Файл | Назначение |
|------|------------|
| `templates/admin/base_site.html` | Кастомный шаблон админки |
| `static/css/admin/admin.css` | Фирменные стили админки |
