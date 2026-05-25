from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, FormView
from django.conf import settings
from main.models import Movie, Category, MovieTag
from main.forms import AddMovieForm, UploadFileForm, AIAssistantForm
from main.services import get_ai_response


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
    data = {
        'title': 'О нас — FGM',
    }
    return render(request, 'main/about.html', context=data)

def sources(request):
    data = {
        'title': 'Источники — FGM'
    }
    return render(request, 'main/sources.html', context=data)

def contact(request):
    data = {
        "title": "Контакты — FGM",
        "api_key": settings.YANDEX_MAPS_API_KEY,
        "coords": settings.STUDIO_COORDINATES
    }
    return render(request, "main/contact.html", context=data)


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


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = AddMovieForm
    template_name = "main/addpage.html"
    success_url = reverse_lazy("home")
    extra_context = dict(title="Добавление фильма")
    permission_required = "main.add_movie"

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

class UpdatePage(PermissionRequiredMixin, UpdateView):
    model = Movie
    form_class = AddMovieForm
    template_name = "main/addpage.html"
    success_url = reverse_lazy("home")
    extra_context = dict(title="Редактирование фильма")
    permission_required = "main.change_movie"

class AIAssistantView(LoginRequiredMixin, FormView):
    template_name = "main/ai_assistant.html"
    form_class = AIAssistantForm
    extra_context = dict(title="ИИ-Ассистент продюсера")

    def form_valid(self, form):
        prompt = form.cleaned_data["prompt"]
        response = get_ai_response(prompt)
        context = self.get_context_data(form=form)
        context["ai_response"] = response
        context["prompt"] = prompt
        return self.render_to_response(context)

