from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe

from .models import News, Category, TagPost


@admin.register(News)
class newsadmin(admin.ModelAdmin):
    fields = ['title', 'content', 'photo', 'post_photo', 'slug', 'cat', 'tag']
    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug': ('title',)}
    filter_vertical = ['tag']
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat',)
    list_display_links = ('title',)
    ordering = ['time_create', ]
    list_editable = ('is_published',)
    actions = ['set_published', 'set_unpublished', ]
    search_fields = ['title__startswith', 'cat__name']
    list_filter = ['cat__name', 'is_published']
    save_on_top = True

    @admin.display(description='Picture', ordering='content')
    def post_photo(self, news: News):
        if news.photo:
            return mark_safe(f"<img src='{news.photo.url}' width=50>")
        else:
            return 'Does not have a photo!'

    @admin.action(description='Set Published')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=News.Status.PUBLISHED)
        self.message_user(request, f"Changed {count} query")

    @admin.action(description='Set Unpublished')
    def set_unpublished(self, request, queryset):
        count = queryset.update(is_published=News.Status.DRAFT)
        self.message_user(request, f"{count} query drafted", messages.WARNING)


@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['id']


@admin.register(TagPost)
class tagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')
    list_display_links = ('id', 'tag')
    ordering = ['id']
