from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import Movie, Category, MovieTag, TechnicalSpecs


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    prepopulated_fields = dict(slug=["name"])
    search_fields = ("name",)


@admin.register(MovieTag)
class MovieTagAdmin(admin.ModelAdmin):
    list_display = ("tag", "slug")
    prepopulated_fields = dict(slug=["tag"])
    search_fields = ("tag",)


class TechnicalSpecsFilter(admin.SimpleListFilter):
    """Кастомный фильтр по наличию техпаспорта"""
    title = "Наличие техпаспорта"
    parameter_name = "tech_status"

    def lookups(self, request, model_admin):
        return [
            ("filled", "Заполнен"),
            ("empty", "Пусто"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "filled":
            return queryset.filter(specs__isnull=False)
        if self.value() == "empty":
            return queryset.filter(specs__isnull=True)


class TechnicalSpecsInline(admin.StackedInline):
    """Inline для технических характеристик на странице фильма"""
    model = TechnicalSpecs
    extra = 0
    verbose_name = "Технический паспорт"
    verbose_name_plural = "Технические характеристики"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("post_photo", "title", "cat", "brief_info", "time_create", "is_published")
    list_display_links = ("title",)
    list_editable = ("is_published", "cat")
    fields = ("title", "slug", "cat", "content", "tags", "photo")
    search_fields = ("title__startswith", "cat__name")
    list_filter = (TechnicalSpecsFilter, "is_published", "cat", "time_create")
    prepopulated_fields = dict(slug=["title"])
    filter_horizontal = ("tags",)
    inlines = [TechnicalSpecsInline]
    ordering = ["-time_create", "title"]
    list_per_page = 10
    readonly_fields = ("post_photo",)

    @admin.display(description="Постер")
    def post_photo(self, obj):
        """Отображение миниатюры постера в админ-панели"""
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=50>")
        return "Нет постера"

    @admin.display(description="Объем описания")
    def brief_info(self, obj):
        """Аналитическое поле - длина синопсиса"""
        return f"Описание: {len(obj.content)} симв."

    @admin.action(description="Опубликовать выбранные фильмы")
    def set_published(self, request, queryset):
        """Массовое опубликование фильмов"""
        count = queryset.update(is_published=Movie.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} записей.")

    @admin.action(description="Снять с публикации выбранные проекты")
    def set_draft(self, request, queryset):
        """Массовое снятие с публикации"""
        count = queryset.update(is_published=Movie.Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} записей.", level=messages.WARNING)

    actions = ["set_published", "set_draft"]


@admin.register(TechnicalSpecs)
class TechnicalSpecsAdmin(admin.ModelAdmin):
    list_display = ("movie", "resolution", "camera", "color_space")
    search_fields = ("movie__title", "camera")
    list_filter = ("resolution",)
