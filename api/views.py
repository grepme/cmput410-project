from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

from comments.models import Comment
from friends.models import Friend, Follow
from posts.models import Post
from tags.models import Tag
from django.contrib.auth.models import User

# Create your views here.

@login_required
def get_posts(request,page="1"):
    #author/posts
    #author/author_id/posts
    return None


