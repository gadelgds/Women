from django.urls import path, re_path, register_converter
from main import views
from main.converters import FourDigitYearConverter
register_converter(FourDigitYearConverter, 'year4')
urlpatterns = [
path('основа/', views.index, name='home'),
path('cats/<int:cat_id>/', views.categories, name='cats_id'),
path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats_slug'),
path('archive/<year4:year>/', views.archive, name='archive_year'),
path('login/', views.login, name='login'),
]