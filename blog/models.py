# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.contrib import admin
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

class BlogPost(models.Model):
	title = models.CharField(max_length=150)
	body = models.TextField()
	timestamp = models.DateTimeField(editable=False)
	tags = models.ManyToManyField('Tag')
	commentsCounter = models.PositiveIntegerField(default=0,editable=False)

	def incrementComment(self):
		self.commentsCounter += 1
		self.save(update_fields=['commentsCounter'])

	def decrementComment(self):
		self.commentsCounter -= 1
		self.save(update_fields=['commentsCounter'])

	class Meta:
		ordering = ('-timestamp',)

	def save(self, *args, **kwargs):
		if self.id == None:
			self.timestamp = datetime.datetime.today()
		super(BlogPost, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title

class Tag(models.Model):
	name = models.CharField(max_length=30, unique=True)

	class Meta:
		ordering = ('name',)

	def __unicode__(self):
		return self.name

class Comment(models.Model):
	author = models.CharField(max_length=30)
	timestamp = models.DateTimeField(editable=False)
	comment = models.TextField()
	blogPost = models.ForeignKey('BlogPost')

	class Meta:
		ordering = ('timestamp',)

	def save(self, *args, **kwargs):
		if self.id == None:
			self.timestamp = datetime.datetime.today()
			self.blogPost.incrementComment()
		super(Comment, self).save(*args, **kwargs)

@receiver(pre_delete, sender=Comment)
def comment_delete(sender, instance, **kwargs):
	instance.blogPost.decrementComment()


"""Admin Models"""

class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'timestamp',)

class TagAdmin(admin.ModelAdmin):
	list_display = ('name',)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('author','blogPost')

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)


