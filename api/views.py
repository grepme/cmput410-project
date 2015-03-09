from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.db.models import Q

from comments.models import Comment
from friends.models import Friend, Follow
from posts.models import Post
from tags.models import Tag
from django.contrib.auth.models import User

'''
    private = 1
    friend = 2
    FOAF = 3
    server = 4
    public = 5
    visibilityChoices = (
        (private, 'Private'),
        (friend, 'Friend'),
        (FOAF, 'Friend of A Friend'),
        (server, 'Server'),
        (public, 'Public'),
    )
'''

# Create your views here.

@login_required
def get_posts(request,author_id=None,page="0"):
    print(author_id,page)
    #author/posts
    #author/author_id/posts

    # authenticated user
    user = request.user

    # Get all direct friends of the user
    friends = Friend.objects.filter(Q(accepter=user) | Q(requester=user))

    # Get all friend of friends, where we are not friends with them
    friend_of_friend = Friend.objects.filter(Q(accepter__in=friends) | Q(requester__in=friends)).exclude(Q(accepter=user) | Q(requester=user))

    # get all posts from friends with proper visibilty
    # Check if we are direct friends, see if post is visibile by friends or FOAF
    # next check for posts from FOAF, check visibilty FOAF
    # After we can get all public posts
    query = (Q(author__in=friends) & (Q(visibility=2) | Q(visibility=3))) | ( Q(author__in=friend_of_friend) & Q(visibility=3) ) | (Q(visibility=5))

    # user specified a specific user id they want to find
    if author_id is not None:
        query = ( query ) & Q(author_id=author_id)

    return Post.objects.filter(query)



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
