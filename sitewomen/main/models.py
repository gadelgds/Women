from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from PIL import Image
import os


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']


class MovieTag(models.Model):
    tag = models.CharField(max_length=100, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['tag']


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Movie.Status.PUBLISHED)


class Movie(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    
    title = models.CharField(max_length=255, verbose_name="Название фильма")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, default='', verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Синопсис/Описание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=Status.PUBLISHED, choices=Status.choices, verbose_name="Статус")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='movies', verbose_name="Категория")
    tags = models.ManyToManyField('MovieTag', related_name='movies', blank=True, verbose_name="Теги")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Постер фильма")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="posts", null=True, default=None, verbose_name="Автор")
    
    objects = models.Manager()  # Стандартный менеджер
    published = PublishedManager()  # Кастомный менеджер для опубликованных

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'movie_slug': self.slug})

    def save(self, *args, **kwargs):
        """Переопределение save для автоматического изменения размера изображения"""
        super().save(*args, **kwargs)
        
        if self.photo:
            img_path = self.photo.path
            if os.path.exists(img_path):
                with Image.open(img_path) as img:
                    max_size = (800, 800)
                    
                    if img.height > max_size[0] or img.width > max_size[1]:
                        img.thumbnail(max_size, Image.Resampling.LANCZOS)
                        img.save(img_path, optimize=True, quality=85)

    class Meta:
        verbose_name = "Кинопроект"
        verbose_name_plural = "Кинопроекты"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]


class TechnicalSpecs(models.Model):
    movie = models.OneToOneField('Movie', on_delete=models.CASCADE, related_name='specs', verbose_name="Фильм")
    resolution = models.CharField(max_length=50, default="4K", verbose_name="Разрешение")
    camera = models.CharField(max_length=100, verbose_name="Камера")
    color_space = models.CharField(max_length=50, verbose_name="Цветовое пространство")

    def __str__(self):
        return f"Техпаспорт для {self.movie.title}"

    class Meta:
        verbose_name = "Технический паспорт"
        verbose_name_plural = "Технические паспорта"
