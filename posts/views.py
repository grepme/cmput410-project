from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from posts.models import Post
from api.models import Server
from django.contrib.auth.models import User
from django.db.models import Q
from friends.models import Friend
import feedparser
from bs4 import BeautifulSoup
import json
from django.views.decorators.http import require_http_methods
# Create your views here


@login_required
@require_http_methods(["POST"])
def new_post(request, source=None):
    origin = request.build_absolute_uri().strip("new/")

    # If it didn't originate from us on this server
    if not source:
        source = origin

    if request.method == 'POST':

        title = request.POST.get("title", "")

        # Either commonmark or plain
        text_format = request.POST.get("content_type", "")
        if text_format == "commonmark":
            text_format = True
        else:
            text_format = False

        # Visibility needs to be set to an int, we can find this out with the function
        visibility = request.POST.get("visibility", "PRIVATE").upper()
        visibility = Post.get_visibility(visibility)

        text = request.POST.get("text", "")

        # Images are in a dictionary that were encoded in the multipart
        if "upload_image" in request.FILES:
            image = request.FILES['upload_image']
        else:
            image = None

        # Fetch the user that uploaded this
        a = request.profile

        # Make the post object
        p = Post.objects.create(title=title, date=timezone.now(), text=text, image=image, origin=origin,
                                source=source, visibility=visibility, commonmark=text_format, author=a)
        p.save()

        # Update the URL since we know the ID of the post
        p.origin = "{}/{}".format(origin, p.guid)
        p.save()

        # Since this is a view, redirect successfully
        return redirect('/dashboard/')
    else:
        # Accept only POST, otherwise, redirect
        return redirect('/')


@login_required
def delete_post(request, guid):
        try:
            # Try to find the user the post belongs to
            post = Post.objects.get(guid=guid, author=request.profile)
            post.delete()
        except Post.DoesNotExist:
            # Post doesn't exist or they don't have permission to delete it
            pass

        return redirect('/dashboard/')

@login_required
def all_posts(request):
    """AJAX call that will grab all posts that a user can see."""

    # Complex queries abound!
    # https://docs.djangoproject.com/en/1.7/topics/db/queries/#complex-lookups-with-q-objects
    # Any posts that are private and owned, public, are on this server, or are friends, or friends of friends.
    # TODO: Friends of friends improvement. OH GOD MY EYES!
    # TODO: FOAF not working
    # TODO: DAMMIT DJANGO! ALLOW MORE NESTED JOINS!
    # p = Post.objects.filter(Q(visibility=Post.private, author=request.profile) |
    # Q(visibility=Post.public) | Q(visibility=Post.server) |
    #                         Q(visibility=Post.friend, author__accepter=request.profile) |
    #                         Q(visibility=Post.friend, author__requester=request.profile) |
    #                         Q(visibility=Post.FOAF, author__requester__requester=request.profile) |
    #                         Q(visibility=Post.FOAF, author__requester__accepter=request.profile) |
    #                         Q(visibility=Post.FOAF, author__accepter__requester=request.profile) |
    #                         Q(visibility=Post.FOAF, author__accepter__accepter=request.profile)
    #
    # )
    p = Post.objects.filter(Q(visibility=Post.private, author=request.profile) |
                            Q(visibility=Post.public) | Q(visibility=Post.server) |
                            Q(visibility=Post.friend, author__accepter=request.profile) |
                            Q(visibility=Post.friend, author__requester=request.profile) |
                            Q(visibility=Post.FOAF, author__requester__requester=request.profile) |
                            Q(visibility=Post.FOAF, author__requester__accepter=request.profile) |
                            Q(visibility=Post.FOAF, author__accepter__requester=request.profile) |
                            Q(visibility=Post.FOAF, author__accepter__accepter=request.profile)

    )

    remote_posts = []
    # Get all remote posts
    for remote_server in Server.objects.all():
        posts = remote_server.get_posts()
        if posts is not None:
            remote_posts.append(posts)

    # Nested query lookups aren't supported, so we need to make multiple queries :(
    return render(request, 'posts/all.html', {'posts': p, 'remote': remote_posts})


@login_required
def my_posts(request):
    """AJAX call that returns the user's posts"""
    p = Post.objects.filter(author=request.profile)
    return render(request, 'posts/all.html', {'posts': p})

@login_required
def new_github_post(request, source=None):
    origin = request.build_absolute_uri().strip("new/")

    # Profile object to save
    user = request.profile
    github = user.github_name

    d = feedparser.parse("http://github.com/" + github + ".atom")

    title = d.entries[0].title
    link = d.entries[0].link

    summary = d.entries[0].summary
    parsed_html = BeautifulSoup(summary)
    if (str(parsed_html.blockquote)=="None"):
        text = "None"
    else:
        text = str(parsed_html.blockquote.string).strip()

    text_format = False

    visibility = Post.get_visibility('PUBLIC')

    image = None

    source = origin


    # Make the post object
    p = Post.objects.create(title=title, date=timezone.now(), text=text, image=image, origin=origin,
                            source=source, visibility=visibility, commonmark=text_format, author=user)
    p.save()

    # Update the URL since we know the ID of the post
    p.origin = "{}/{}".format(origin, p.guid)
    p.save()

    # Since this is a view, redirect successfully
    return redirect('/dashboard/')
