# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
	url(r'^filter$', 'archive'),
	url(r'^post/(?P<id>\d+)/$', 'viewBlogPost'),
    #url(r'$', 'archive'),
    )