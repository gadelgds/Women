from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse

def index(request):
    posts = [
        {'id': 1, 'title': 'Новый проект в разработке', 'content': 'Мы рады объявить о начале работы над новым блокбастером. Съемки начнутся в следующем квартале с участием звездного актерского состава.', 'is_published': True},
        {'id': 2, 'title': 'Обновление платформы FGM', 'content': 'Вышла новая версия системы управления проектами. Теперь доступны расширенные возможности для координации съемочных групп и автоматизации рабочих процессов.', 'is_published': True},
        {'id': 3, 'title': 'Внутренний тест', 'content': 'Этот пост находится в разработке и не должен быть виден публично. Тестирование новых функций продолжается.', 'is_published': False},
        {'id': 4, 'title': 'Успешное завершение проекта', 'content': 'Наша команда успешно завершила работу над фильмом, который выйдет в прокат этим летом. Благодарим всех участников за профессионализм и слаженную работу.', 'is_published': True},
    ]
    
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
