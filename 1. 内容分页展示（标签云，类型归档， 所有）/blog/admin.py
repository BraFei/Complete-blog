from django.contrib import admin
from .models import Category, Tag, Blog


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'author', 'created', 'update']
