from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from main.models import Movie

def index(request):
    posts = Movie.published.all()
    
    data = {
        'title': 'FGM — Управление кинопроизводством',
        'posts': posts
    }
    return render(request, 'main/index.html', context=data)

def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p >id:{cat_id}</p>")

def categories_by_slug(request, cat_slug):
    print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p >Слаг:{cat_slug}</p>")

def archive(request, year):
    if year > 2027:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1><p>Год:{year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def login(request):
    return HttpResponse('<h1>Страница логина</h1>')

def about(request):
    data = {
        'title': 'О нас — FGM'
    }
    return render(request, 'main/about.html', context=data)

def sources(request):
    data = {
        'title': 'Источники — FGM'
    }
    return render(request, 'main/sources.html', context=data)


def show_movie(request, movie_slug):
    movie = get_object_or_404(Movie, slug=movie_slug)
    
    data = {
        'title': movie.title,
        'movie': movie
    }
    return render(request, 'main/movie_detail.html', context=data)
