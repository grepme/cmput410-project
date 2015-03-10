from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.core import serializers
import logging
import json


from comments.models import Comment
from friends.models import Friend, Follow
from posts.models import Post, PostEncoder
from tags.models import Tag
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


#TODO Move to another file...
from functools import wraps
from django.utils.decorators import available_attrs
logger = logging.getLogger('django.request')

def require_http_accept(request_accept_list):
    """
    Decorator to make a view only accept particular requests with Accept types.  Usage:

        @require_http_accept(["application/json", "text/html"])
        def my_view(request):
            # I can assume now that only requests with accepts within the list make it this far
            # ...

    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):

            list_extra = list(request_accept_list)
            list_extra.append('*/*')

            accept = request.META.get('Accept')

            # none condition we assume */*
            if accept not in request_accept_list and accept is not None:
                logger.warning('Accept Not Allowed (%s): %s', request.META.get('Accept'), request.path,
                    extra={
                        'status_code': 406,
                        'request': request
                    }
                )
                response = HttpResponse("Accept Not Allowed (%s): %s", request.META.get('Accept'), request.path)
                response.status_code = 406
                return response
            return func(request, *args, **kwargs)
        return inner
    return decorator

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
@require_http_accept(['application/json'])
def get_posts(request,author_id=None,page="0"):
    #author/posts
    #author/author_id/posts

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

    # Check if user is valid
    # TODO Decorator?
    if author_id is not None:
        try:
            User.objects.get(id=author_id)
        except User.DoesNotExist as e:
            # return a better error for missing user
            response = JsonResponse({"message":"Author with id %d does not exist" % author_id})
            response.status_code = 404
            return response

    posts_query = Post.objects.filter(query)
    posts = list(obj.as_dict() for obj in posts_query)

    #TODO Add Pagination
    data = {"posts":posts};

    return JsonResponse(data)

def get_post(request,post_id=None,page="0"):
    if post_id is not None:
        try:
            post = Post.objects.get(post_id)
        except Post.DoesNotExist as e:
            response = JsonResponse({"message":"Post with id %d does not exist" % post_id})
            response.status_code = 404
            return response

    else:
        return Post.objects.filter(visibility=Post.public).order_by('-date')

def friend_request(request,page="1"):
    return None

def get_friends(request,page="1"):
    return None

def is_friend(request,page="1"):
    return None
