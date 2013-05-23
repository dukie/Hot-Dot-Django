# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.shortcuts import render
from blog.models import BlogPost
from blog.models import Comment
from blog.forms import AddCommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def archive(request):
    if request.method == 'GET':
        tag = request.GET.get('tag')
        if tag:
            posts = BlogPost.objects.filter(tags__name__contains=tag)
        else:
            posts = BlogPost.objects.all()
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, 'archive.html', {'posts': posts})

def viewBlogPost(request,id):
    try:
        blogPost = BlogPost.objects.get(pk=id)
        comments = Comment.objects.filter(blogPost = blogPost)
        if request.method == 'POST':
            form = AddCommentForm(request.POST)
            if form.is_valid():
                newComment = Comment()
                newComment.blogPost = blogPost
                newComment.author = form.cleaned_data['author']
                newComment.comment = form.cleaned_data['message']
                newComment.save()
        else:
            form = AddCommentForm(initial={'blogPost': blogPost})
        return render(request, 'blogentry.html',{'post': blogPost, 'comments': comments, 'form':form})
    except BlogPost.DoesNotExist:
        return redirect('blog.views.archive')

