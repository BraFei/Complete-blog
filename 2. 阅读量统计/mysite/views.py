# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Blog, Category, Tag
from read_statistics.utils import get_seven_days_read_data
from django.contrib.contenttypes.models import ContentType


# 获取分页
def get_paginator_data(req, object_list):
	paginator = Paginator(object_list, 5)
	page = req.GET.get('page', 1)
	
	try:
		page_of_list = paginator.page(page)
	except PageNotAnInteger:
		page_of_list = paginator.page(1)
	except EmptyPage:
		page_of_list = paginator(paginator.num_pages)
	current_page_num = page_of_list.number
	page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
		range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
	
	if page_range[0] - 1 > 2:
		page_range.insert(0, '...')
	
	if paginator.num_pages - page_range[-1] >= 2:
		page_range.append('...')
	
	if page_range[0] != 1:
		page_range.insert(0, 1)
	if page_range[-1] != paginator.num_pages:
		page_range.append(paginator.num_pages)
	context = dict()
	context['lists'] = page_of_list.object_list
	context['page_list'] = page_of_list
	context['page_range'] = page_range
	return context


# Create your views here.
def index(req):
	blog_list = Blog.published.all()
	context = get_paginator_data(req, blog_list)
	context['blog_list'] = context['lists']
	context['page_of_blogs'] = context['page_list']
	
	blog_content_type = ContentType.objects.get_for_model(Blog)
	dates, read_nums = get_seven_days_read_data(blog_content_type)
	context['dates'] = dates
	context['read_nums'] = read_nums
	return render(req, 'index.html', context)


def feeling(req):
	blog_content_type = ContentType.objects.get_for_model(Blog)
	dates, read_nums = get_seven_days_read_data(blog_content_type)
	context = dict()
	context['dates'] = dates
	context['read_nums'] = read_nums
	return render(req, 'feeling.html', context)
