# -*- coding: utf-8 -*-
from django import forms
from blog.models import Comment
from blog.models import BlogPost

class AddCommentForm(forms.Form):
	author = forms.CharField(max_length=30)
	message = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = Comment