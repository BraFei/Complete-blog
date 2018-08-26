from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from read_statistics.models import ReadNumExpandMethod, ReadDetail
from django.contrib.contenttypes.fields import GenericRelation


class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')


# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=10)
	
	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=10)
	
	def __str__(self):
		return self.name


class Blog(models.Model, ReadNumExpandMethod):
	STATUS_CHOICES = (
		('draft', 'Draft'), ('published', 'Published'),)
	title = models.CharField(max_length=30)
	content = models.TextField()
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	tag = models.ManyToManyField(Tag)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	read_details = GenericRelation(ReadDetail)
	thumbnail = models.ImageField(upload_to='blog/%Y/%m/%d', blank=True)
	created = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	publish = models.DateTimeField(default=timezone.now)
	
	objects = models.Manager()
	published = PublishedManager()
	
	def __str__(self):
		return self.title
	
	class Meta:
		ordering = ['-created']

