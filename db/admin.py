from django.contrib import admin
from .models import Corpus, Text


# --- Настройка отображения таблицы Corpus ---
@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'description')
    search_fields = ('title', 'genre')
    list_filter = ('genre',)
    ordering = ('title',)


# --- Настройка отображения таблицы Text ---
@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'corpus', 'has_translation')
    search_fields = ('title', 'description', 'content')
    list_filter = ('corpus',)
    ordering = ('title',)
