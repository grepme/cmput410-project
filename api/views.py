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
from user_profile.models import Profile
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
                response = HttpResponse("Accept Not Allowed ({}): {}".format(request.META.get('Accept'), request.path))
                response.status_code = 406
                return response
            return func(request, *args, **kwargs)
        return inner
    return decorator

def http_error_code(code,message):
    """
    Decorator to return Not Implemented HTTP error Code usage:

        @http_error_code(501,"Not Implemented")
        def my_view(request):
            # I can assume now that only requests with accepts within the list make it this far
            # ...

    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            logger.warning("%s : %s",message, request.path,
                    extra={
                        'status_code': code,
                        'request': request
                    }
                )
            response = HttpResponse("{} : {}".format(message, request.path))
            response.status_code = code
            return response
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

def get_post_query(request):
        return ( Q(visibility=Post.private, author__username=request.user.username) |
        Q(visibility=Post.public) | Q(visibility=Post.server) |
        Q(visibility=Post.friend, author__accepter=request.user.id, author__accepter__accepted=True) |
        Q(visibility=Post.friend, author__requester=request.user.id, author__accepter__accepted=True) |
        Q(visibility=Post.FOAF, author__requester__requester=request.user.id, author__accepter__accepted=True) |
        Q(visibility=Post.FOAF, author__requester__accepter=request.user.id, author__accepter__accepted=True) |
        Q(visibility=Post.FOAF, author__accepter__requester=request.user.id, author__accepter__accepted=True) |
        Q(visibility=Post.FOAF, author__accepter__accepter=request.user.id, author__accepter__accepted=True) )

def model_list(model_query):
    return list(obj.as_dict() for obj in model_query)

def has_keys(keys,dictionary,main_key):
    if all ("{}[{}]".format(main_key,key) in dictionary for key in keys):
        return True
    return False



@login_required
@require_http_methods(["GET"])
@require_http_accept(['application/json'])
def get_posts(request,author_id=None,page="0"):

    #author/posts
    #author/author_id/posts

    query = get_post_query(request)

    # user specified a specific user id they want to find
    if author_id is not None and author_id != request.user.id:
        query = ( query ) & Q(author_id=author_id)
    elif author_id is not None:
        # author id = same user
        query = Q(author_id=request.user.guid)

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
    print(posts_query.query)
    posts = model_list(posts_query)

    #TODO Add Pagination
    data = {"posts":posts};

    return JsonResponse(data)

@login_required
@require_http_methods(["GET"])
@require_http_accept(['application/json'])
def get_post(request,post_id=None,page="0"):
    return_data = list()
    if post_id is not None:

        query = get_post_query(request) & Q(guid=post_id)
        posts_query = Post.objects.filter(query)
        return_data = model_list(posts_query)

        if len(posts_query) == 0:
            response = JsonResponse({"message":"Post with id %d does not exist" % post_id})
            response.status_code = 404
            return response

    else:
        posts_query = Post.objects.filter(visibility=Post.public).order_by('-date')
        return_data = model_list(posts_query)

    # TODO Add pagination
    return JsonResponse({"posts":return_data})

#@login_required
@require_http_methods(["POST"])
@require_http_accept(['application/json'])
#@http_error_code(501,"Not Implemented")
def friend_request(request,page="0"):
    # get data from request
    data = request.POST.dict()
    keys = ['id','host','url','displayname']

    if has_keys(keys,data,'author') and has_keys(keys,data,'friend'):
        author = Profile.objects.get(guid=data["author[id]"])
        friend = Profile.objects.get(guid=data["friend[id]"])

        if author == None:
            author = data["author[id]"]
        else:
            author = author.author

        if friend == None:
            friend = data["friend[id]"]
        else:
            friend = friend.author

        if author == friend:
            return HttpResponse(400)

        found = Friend.objects.filter(Q(requester_id=author,accepter_id=friend) | Q(requester_id=friend,accepter_id=author))

        if found is not None:

            if len(found) == 1:
                print "FOUND ITEM"
                found = found[0]
                found.accepted = True
                found.save()
            else:
                print Friend.objects.create(requester=author,accepter=friend)
                print Follow.objects.create(follower=author,following=friend)

            return HttpResponse(200)

        return HttpResponse(400)


#@login_required
@require_http_methods(["POST"])
@require_http_accept(['application/json'])
#@http_error_code(501,"Not Implemented")
def get_friends(request,page="0"):

    # get all accepted friends
    friends = Friend.objects.filter(Q(requester=user,accept=True) | Q(accepter=user,accept=True))
    return_data = model_list(friends)
    return JsonResponse({"":return_data})


#@login_required
#@require_http_methods(["GET"])
#@require_http_accept(['application/json'])
@http_error_code(501,"Not Implemented")
def is_friend(request,page="0"):
    return None

@require_http_methods(["GET"])
@require_http_accept(['application/json'])
def search_users(request,name=""):
    profile_query = Profile.objects.filter(display_name__icontains=name)
    return JsonResponse({"users":model_list(profile_query)})


