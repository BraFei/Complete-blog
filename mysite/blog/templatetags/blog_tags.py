from django import template
from ..models import Blog, Tag, Category


register = template.Library()


@register.simple_tag
def total_blogs():
	return Blog.published.count()


@register.simple_tag
def get_recent_blogs(num=6):
	return Blog.published.all()[:num]


@register.simple_tag
def get_all_tags():
	return Tag.objects.all()


@register.simple_tag
def get_all_categories():
	return Category.objects.all()


@register.simple_tag
def get_blogs_with_date():
	return Blog.published.dates('publish', 'month', order='DESC')
