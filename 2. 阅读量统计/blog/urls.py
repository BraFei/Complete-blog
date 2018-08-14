from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='blog_list'), path('details/<int:blog_id>', blog_detail, name='blog_detail'),
    path('date/<int:blog_year>/<int:blog_month>', blogs_with_date, name='blogs_with_date'),
	path('category/<int:category_pk>', blogs_with_category, name='blogs_with_category'),
	path('categories/<int:blog_pk>', blogs_with_categories, name='blogs_with_categories'),
	path('tag/<int:tag_pk>', blogs_with_tag, name='blogs_with_tag'),
]
