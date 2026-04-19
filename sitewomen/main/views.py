from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse

def index(request):
    return render(request, 'main/index.html')

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
