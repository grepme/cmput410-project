from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.core import serializers
import json
import pickle

from comments.models import Comment
from friends.models import Friend, Follow
from posts.models import Post
from tags.models import Tag
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Create your views here.

def check_accept_type(content_type):
    supported_content_types = ['*/*' , 'application/json']
    for supported_type in supported_content_types:
        if content_type == supported_type:
            return True
    return False

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, set):
          return list(obj)
       return json.JSONEncoder.default(self, obj)


@login_required
@require_http_methods(["GET"])
def get_posts(request,author_id=None,page="0"):
    #author/posts
    #author/author_id/posts

    #assume */*
    valid_accept = True

    # check specificed content
    if 'ACCEPT' in request.META:
        accept_type = request.META['ACCEPT']
        valid_accept = check_accept_type(accept_type)

    if valid_accept:
        query = ( Q(visibility=Post.private, author__username=request.user.username) |
                Q(visibility=Post.public) | Q(visibility=Post.server) |
                Q(visibility=Post.friend, author__accepter=request.user.id) |
                Q(visibility=Post.friend, author__requester=request.user.id) |
                Q(visibility=Post.FOAF, author__requester__requester=request.user.id) |
                Q(visibility=Post.FOAF, author__requester__accepter=request.user.id) |
                Q(visibility=Post.FOAF, author__accepter__requester=request.user.id) |
                Q(visibility=Post.FOAF, author__accepter__accepter=request.user.id) )

        # user specified a specific user id they want to find
        if author_id is not None and author_id != request.user.id:
            query = ( query ) & Q(author_id=author_id)
        elif author_id is not None:
            # author id = same user
            query = Q(author_id=request.user.id)

        posts = Post.objects.filter(query)
        posts = serializers.serialize("json", posts)

        #TODO Add Pagination
        data = {"posts":posts};

        return JsonResponse(data)
    else:
        return HttpResponse(status_code=406)

def get_post(request,post_id=None,page="0"):
    if post_id is not None:
        return Post.objects.get(post_id)
    else:
        # TODO: Import these enum visibilities
        # I don't like hardcoding...
        return Post.objects.filter(visibility=5).order_by('-date')

def friend_request(request,page="1"):
    return None

def get_friends(request,page="1"):
    return None

def is_friend(request,page="1"):
    return None
