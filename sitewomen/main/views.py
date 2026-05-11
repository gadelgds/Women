from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from main.models import Movie, Category, MovieTag
from main.forms import AddMovieForm, UploadFileForm


def index(request):
    posts = Movie.published.select_related('cat').all()
    
    data = {
        'title': 'FGM — Управление кинопроизводством',
        'posts': posts,
        'cat_selected': 0
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
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()
    
    data = {
        'title': 'О нас — FGM',
        'form': form
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


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Movie.published.select_related('cat').filter(cat_id=category.pk)
    
    data = {
        'title': category.name,
        'posts': posts,
        'cat_selected': category.pk
    }
    return render(request, 'main/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(MovieTag, slug=tag_slug)
    posts = tag.movies.filter(is_published=Movie.Status.PUBLISHED)
    
    data = {
        'title': tag.tag,
        'posts': posts,
        'cat_selected': None
    }
    return render(request, 'main/index.html', context=data)


def addpage(request):
    if request.method == 'POST':
        form = AddMovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddMovieForm()
    
    menu = [
        {'title': 'Каталог', 'url_name': 'home'},
        {'title': 'Тарифы', 'url_name': 'home'},
        {'title': 'Источники', 'url_name': 'sources'},
        {'title': 'О нас', 'url_name': 'about'},
    ]
    
    data = {
        'title': 'Добавление фильма',
        'menu': menu,
        'form': form
    }
    return render(request, 'main/addpage.html', context=data)
