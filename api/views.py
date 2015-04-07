from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.core import serializers
import logging
import json

from api.models import Server

from comments.models import Comment
from django.db import IntegrityError
from user_profile.models import Profile
from friends.models import Friend, Follow
import friends.views
from posts.models import Post, PostEncoder
from tags.models import Tag
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


# TODO Move to another file...
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
            if accept not in list_extra and accept is not None:
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

def auth_as_user():
    """
        Fake user auth for api
    """

    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            profile = None
            try:
                user_guid = request.META.get('HTTP_USER')
                profile = Profile.objects.get(guid=user_guid)
                request.profile = profile
            except Profile.DoesNotExist as e:
                if request.user.is_authenticated():
                    profile = Profile.objects.get(author=request.user)
                else:
                    logger.warning('Not Authenticated (%s): %s', request.META.get('HTTP_USER'), request.path,
                                   extra={
                                       'status_code': 401,
                                       'request': request
                                   }
                    )
                    return JsonUnauthorized()
            return func(request, *args, **kwargs)

        return inner

    return decorator


def require_http_content_type(request_accept_list):
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

            content_type = request.META.get('Content-Type')

            # none condition we assume */*
            if content_type not in list_extra and content_type is not None:
                logger.warning('Content-Type Not Allowed (%s): %s', request.META.get('Content-Type'), request.path,
                               extra={
                                   'status_code': 406,
                                   'request': request
                               }
                )
                response = HttpResponse(
                    "Content-Type Not Allowed ({}): {}".format(request.META.get('Content-Type'), request.path))
                response.status_code = 406
                return response
            return func(request, *args, **kwargs)

        return inner

    return decorator


def http_error_code(code, message):
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
            logger.warning("%s : %s", message, request.path,
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
    supported_content_types = ['*/*', 'application/json']
    for supported_type in supported_content_types:
        if content_type == supported_type:
            return True
    return False


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def get_other_friends(friends, query):
    profiles = list()
    for query_item in query:
        if query_item.accepter in friends:
            profiles.append(query_item.requester)
        else:
            profiles.append(query_item.accepter)
    return profiles


def get_post_query(request):

        # All people I follow
    following = Follow.objects.filter(follower=request.profile)

    # My Friends
    friends = Friend.objects.filter(Q(requester=request.profile) | Q(accepter=request.profile))

    # The Friends Profile
    friends = get_other_profiles(request.profile,friends)

    # Get my Friends of Friends
    friends_friends = Friend.objects.filter(Q(requester__in=friends) | Q(accepter__in=friends))

    # Get the other friends..
    friends_friends = get_other_friends(friends,friends_friends)

    return (Q(author=request.profile) | Q(visibility=Post.public) |
                                Q(visibility=Post.friend, author__requester=request.profile) |
                                Q(visibility=Post.friend, author__accepter=request.profile) |
                                Q(visibility=Post.FOAF, author__requester=request.profile)|
                                Q(visibility=Post.FOAF, author__accepter=request.profile) |
                                Q(author__in=friends_friends,visibility=Post.FOAF))

    '''return  (Q(visibility=Post.private, author=request.profile) |
                            Q(visibility=Post.public) |
                            Q(visibility=Post.friend, author__accepter=request.profile) |
                            Q(visibility=Post.friend, author__requester=request.profile) |
                            Q(visibility=Post.FOAF, author__requester__requester=request.profile) |
                            Q(visibility=Post.FOAF, author__requester__accepter=request.profile) |
                            Q(visibility=Post.FOAF, author__accepter__requester=request.profile) |
                            Q(visibility=Post.FOAF, author__accepter__accepter=request.profile))
    '''


def model_list(model_query):
    return list(obj.as_dict() for obj in model_query)


def has_keys(keys, dictionary, main_key):
    if all(key in dictionary[main_key] for key in keys):
        return True
    return False


def compare(s, t):
    return Counter(s) == Counter(t)

def JsonNotFound(model,model_id):
    response = JsonResponse({"message": "{} with id {} does not exist".format(model,model_id)})
    response.status_code = 404
    return response

def JsonBadRequest():
    response = JsonResponse({"message": "Malformed request data"})
    response.status_code = 400
    return response

def JsonUnauthorized():
    response = JsonResponse({"message": "Unauthorized"})
    response.status_code = 401
    return response


# Profile = User Who is trying to get post
# Author = Author of the Post we are trying to get
# Friends list of Friends, for that profile
def get_foaf_servers(profile, author, friends):
    # Find the server we defined as host, check for contains to be safe...
    current_server = Server.objects.filter(host__icontains=profile["host"]).first()

    friends_profiles = Profile.objects.filter(guid__in=friends)

    if current_server is not None:
        result = current_server.get_friends_list(profile, friends)

        # Ok to Proceed
        if not compare(result["friends"], friends):
            return False


    # Check if the Author is
    try:
        friends_query = Friend.objects.filter(Q(accepter=author, requester__in=friends_profiles) | Q(requester=author, accepter__in=friends_profiles))
    except Exception as e:
        print e

    # Extract just the guids
    friends = get_other_profiles(author, friends_query)

    servers = Server.objects.all()
    if len(friends) > 0:
        for server in servers:
            for friend in friends:
                if len(server.get_friends_list(profile["id"], friends)["friends"]) > 0:
                    return True
    else:
        return False

    if len(servers) == 0:
        return True


@auth_as_user()
@require_http_methods(["GET"])
@require_http_accept(['application/json'])
@require_http_content_type(['application/json'])
def get_posts(request, author_id=None, page="0"):
    # author/posts
    #author/author_id/posts

    query = get_post_query(request)

    # user specified a specific user id they want to find
    if author_id is not None and author_id != request.profile.guid:
        query = ( query ) & Q(author__guid=author_id)
    elif author_id is not None:
        # author id = same user
        query = Q(author__guid=request.profile.guid)

    # Check if user is valid
    # TODO Decorator?
    if author_id is not None:
        try:
            Profile.objects.get(guid=author_id)
        except Profile.DoesNotExist as e:
            return JsonNotFound("Author",author_id)

    posts_query = Post.objects.filter(query).distinct()
    posts = model_list(posts_query)

    # TODO Add Pagination
    data = {"posts": posts}

    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["GET", "POST"])
@require_http_accept(['application/json'])
@require_http_content_type(['application/json'])
def get_post(request, post_id=None, page="0"):

    if request.method == "POST":
        data = None
        post = None
        try:
            data = json.loads(request.body)
        except ValueError as e:
            return JsonBadRequest()

        try:
            post = Post.objects.get(guid=post_id)
        except Exception as e:
            return JsonNotFound("Post",post_id)

        post_author = post.author

        keys = ['id', 'host', 'displayname']
        if has_keys(keys, data, 'author') and 'friends' in data:
            author = data["author"]

            if not get_foaf_servers(author, post_author, data["friends"]):
                return JsonUnauthorized()
            else:
                return JsonResponse({"posts": [post.as_dict()]})

    return_data = list()
    if post_id is not None and request.user.is_authenticated():

        query = (get_post_query(request) & Q(guid=post_id))

        posts_query = Post.objects.filter(query).distinct()
        return_data = model_list(posts_query)

        if len(posts_query) == 0:
            return JsonNotFound("Post",post_id)

    else:
        posts_query = Post.objects.filter(visibility=Post.public).order_by('-date').distinct()
        return_data = model_list(posts_query)

        # TODO Add pagination
    return JsonResponse({"posts": return_data})


@csrf_exempt
@require_http_methods(["POST"])
@require_http_accept(['application/json'])
@require_http_content_type(['application/json'])
def friend_request(request, page="0"):
    return(friends.views.friend_request(request, page))

@csrf_exempt
@require_http_methods(["GET"])
@require_http_accept(['application/json'])
@require_http_content_type(['application/json'])
def get_authors(request):
    # get all accepted friends
    profiles = model_list(Profile.objects.all())
    # for profile in profiles:
        # delete github_username?

    return JsonResponse({"authors": profiles})

@csrf_exempt
@require_http_methods(["GET"])
@require_http_accept(['application/json'])
@require_http_content_type(['application/json'])
def get_author(request,profile_id):
    # get all accepted friends
    profile = None
    try:
        profile = Profile.objects.get(guid=profile_id)
    except Profile.DoesNotExist as e:
        return JsonNotFound("Profile",profile_id)

    friends = Friend.objects.filter(Q(accepter=profile) | Q(requester=profile))

    friends = model_list(get_other_friends(profile,friends))

    profile_dict = profile.as_dict()

    profile_dict["friends"] = friends

    return JsonResponse(profile_dict)


#TODO PUT THIS IN COMMON PLACE THIS IS FROM
# THE FRIENDS APP
def get_other_profiles(profile, query):
    profiles = list()

    for query_item in query:
        if query_item.accepter == profile:
            profiles.append(query_item.requester.guid)
        else:
            profiles.append(query_item.accepter.guid)
    return profiles


@csrf_exempt
@require_http_methods(["POST"])
@require_http_accept(['application/json'])
@require_http_content_type(['application/json'])
#@http_error_code(501,"Not Implemented")
def get_friends(request, author_id=None, page="0"):
    data = None
    author = None
    try:
        data = json.loads(request.body)
    except ValueError as e:
        return JsonBadRequest()

    if data['author'] is not None and data['authors'] is not None:
        # List of authors
        friends_list = data['authors']

        try:
            author = Profile.objects.get(guid=data['author'])
        except Profile.DoesNotExist as e:
            return JsonNotFound("Profile",data["author"])

        if author.guid != author_id:
            return JsonBadRequest()
    else:
        return JsonBadRequest()

    profile_list = Profile.objects.filter(guid__in=friends_list)

    # get all accepted friends
    friends = Friend.objects.filter(
        Q(requester__in=profile_list, accepter=author) | Q(accepter__in=profile_list,requester=author))

    return_friends = get_other_profiles(author, friends)

    return JsonResponse({"query": "friends", "author": author.guid, "friends": return_friends})


@login_required
@require_http_methods(["POST"])
@require_http_accept(['application/json'])
@require_http_content_type(['application/json'])
def follow_user(request):
    return(friends.views.follow_user(request))


@require_http_methods(["GET"])
@require_http_accept(['application/json'])
@require_http_content_type(['application/json'])
def is_friend(request, author_id=None, author_2_id=None, page="0"):
    response_data = {"query": "friends", "authors": [author_id, author_2_id]}

    author = None
    author_2 = None

    try:
        author = Profile.objects.get(guid=author_id)
    except Profile.DoesNotExist as e:
        response = JsonResponse({"message": "Author with id {} does not exist".format(author_id)})
        response.status_code = 404
        return response

    try:
        author_2 = Profile.objects.get(guid=author_2_id)
    except:
        pass

    friend = Friend.objects.filter(Q(requester=author,  accepter=author_2) | Q(accepter=author, requester=author_2)).first()

    if friend is not None:
        response_data["friends"] = "YES"
    else:
        response_data["friends"] = "NO"

    return JsonResponse(response_data)


@require_http_methods(["GET"])
@require_http_accept(['application/json'])
@require_http_content_type(['application/json'])
def search_users(request, name=""):
    profile_query = Profile.objects.filter(display_name__icontains=name)
    return JsonResponse({"users": model_list(profile_query)})


