from django.urls import path
from .views import index, blog_detail, blogs_with_date, blogs_with_category, blogs_with_categories

urlpatterns = [
    path('', index, name='index'), path('details/<int:blog_id>', blog_detail, name='blog_detail'),
    path('date/<int:blog_year>/<int:blog_month>', blogs_with_date, name='blogs_with_date'),
	path('category/<int:category_pk>', blogs_with_category, name='blogs_with_category'),
	path('categories/<int:blog_pk>', blogs_with_categories, name='blogs_with_categories'),
]
