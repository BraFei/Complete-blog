# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Blog, Category, Tag
import markdown
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
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
	return render(req, 'blog/post_list.html', context)


def blog_detail(req, blog_id):
	blog = get_object_or_404(Blog, id=blog_id)
	blog.content = markdown.markdown(
		blog.content, extensions=[
			'markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc'])
	read_cookie_key = read_statistics_once_read(req, blog)
	
	context = dict()
	context['blog'] = blog
	context['blog_tags'] = blog.tag.all()
	context['pre_blog'] = Blog.published.filter(publish__gt=blog.publish).last()
	context['next_blog'] = Blog.published.filter(publish__lt=blog.publish).first()
	
	response = render(req, 'blog/blog_detail.html', context)
	response.set_cookie(read_cookie_key, 'true')
	return response


def blogs_with_date(req, blog_year, blog_month):
	blog_list = Blog.published.filter(publish__year=blog_year, publish__month=blog_month)
	context = get_paginator_data(req, blog_list)
	context['blog_list'] = context['lists']
	context['page_of_blogs'] = context['page_list']
	return render(req, 'blog/post_list.html', context)


def blogs_with_category(req, category_pk):
	category = get_object_or_404(Category, id=category_pk)
	blog_list = Blog.published.filter(category=category)
	context = get_paginator_data(req, blog_list)
	context['blog_list'] = context['lists']
	context['page_of_blogs'] = context['page_list']
	return render(req, 'blog/post_list.html', context)


def blogs_with_categories(req, blog_pk):
	blog = get_object_or_404(Blog, id=blog_pk)
	blog_list = Blog.published.filter(category=blog.category)
	context = get_paginator_data(req, blog_list)
	context['blog_list'] = context['lists']
	context['page_of_blogs'] = context['page_list']
	return render(req, 'blog/post_list.html', context)


def blogs_with_tag(req, tag_pk):
	tag = get_object_or_404(Tag, id=tag_pk)
	blog_list = tag.blog_set.filter(status='published')
	context = get_paginator_data(req, blog_list)
	context['blog_list'] = context['lists']
	context['page_of_blogs'] = context['page_list']
	return render(req, 'blog/post_list.html', context)