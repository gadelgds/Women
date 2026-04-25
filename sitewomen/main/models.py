from django.db import models
from django.urls import reverse


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
    
    objects = models.Manager()  # Стандартный менеджер
    published = PublishedManager()  # Кастомный менеджер для опубликованных

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'movie_slug': self.slug})

    class Meta:
        verbose_name = "Кинопроект"
        verbose_name_plural = "Кинопроекты"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]
