from django.contrib import admin
from .models import Movie, TechnicalSpecs


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'time_update', 'is_published')
    list_filter = ('is_published', 'time_create')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    ordering = ('-time_create',)


@admin.register(TechnicalSpecs)
class TechnicalSpecsAdmin(admin.ModelAdmin):
    list_display = ('movie', 'resolution', 'camera', 'color_space')
    search_fields = ('movie__title', 'camera')
    list_filter = ('resolution',)
