from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .models import Post, Comment

import logging

logger = logging.getLogger('blog.views')

# Create your views here.
def index(request):
    latest_posts = Post.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')

    return render(request, 'index.html', {
        'latest_posts': latest_posts,
    })


def post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post=post_id)
    except ObjectDoesNotExist as objErr:
        logger.error(f'Getting post with ID: {post_id} returned {objErr}')

        return HttpResponse(f'Post {post_id} not found')
    else:
        return render(request, 'post.html', {
            'post': post,
            'comments': comments,
        })


def comment(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post=post_id)

        author = request.POST['author']
        comment_body= request.POST['comment']
    except (KeyError, ObjectDoesNotExist) as err:
        logger.error(f'Posting comment error for {post_id}: {err}')

        return render(request, 'post.html', {
            'post': post,
            'comments': comments,
            'error_message': 'You must leave a name AND a comment.'
        })
    else:
        new_comment = Comment(post=post, author=author, body=comment_body)
        new_comment.save()

        return HttpResponseRedirect(f'/post/{post_id}')