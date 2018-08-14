from django import template
from django.db.models import Sum
from django.core.cache import cache
from ..models import Blog, Tag, Category
import datetime
from read_statistics.models import *

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


@register.simple_tag
def get_yesterday_hot_blogs():
	blog_content_type = ContentType.objects.get_for_model(Blog)
	today = timezone.now().date()
	yesterday = today - datetime.timedelta(days=1)
	return ReadDetail.objects.filter(content_type=blog_content_type, date=yesterday).order_by('-read_num')[:5]


@register.simple_tag
def get_7_days_hot_blogs():
	today = timezone.now().date()
	date = today - datetime.timedelta(days=7)
	blogs = Blog.objects.filter(
		read_details__date__lt=today,
		read_details__date__gte=date)\
		.values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num'))\
		.order_by('-read_num_sum')
	return blogs[:6]


@register.simple_tag
def get_hot_blogs_for_7_days():
	# 获取7天热门博客的缓存数据
	hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
	if hot_blogs_for_7_days is None:
		hot_blogs_for_7_days = get_7_days_hot_blogs()
		cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)
	return hot_blogs_for_7_days
