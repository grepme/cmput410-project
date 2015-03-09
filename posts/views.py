from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from posts.models import Post
from django.contrib.auth.models import User
from django.db.models import Q
from friends.models import Friend

# Create your views here


@login_required
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
        visibility = request.POST.get("visibility", "Private")
        visibility = Post.get_visibility(visibility)

        text = request.POST.get("text", "")

        # Images are in a dictionary that were encoded in the multipart
        if "upload_image" in request.FILES:
            image = request.FILES['upload_image']
        else:
            image = None

        # Fetch the user that uploaded this
        a = User.objects.get(username=request.user.username)

        # Make the post object
        p = Post.objects.create(title=title, date=timezone.now(), text=text, image=image, origin=origin,
                                source=source, visibility=visibility, commonmark=text_format, author=a)
        p.save()

        # Update the URL since we know the ID of the post
        p.origin = "{}/{}".format(origin, p.id)
        p.save()

        # Since this is a view, redirect successfully
        return redirect('/dashboard/')
    else:
        # Accept only POST, otherwise, redirect
        redirect('/')


@login_required
def delete_post(request, guid):
    try:
        # Try to find the user the post belongs to
        post = Post.objects.get(guid=guid, author__username=request.user.username)
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
    # TODO: DAMMIT DJANGO! ALLOW MORE NESTED JOINS!
    p = Post.objects.filter(Q(visibility=Post.private, author__username=request.user.username) |
                            Q(visibility=Post.public) | Q(visibility=Post.server) |
                            Q(visibility=Post.friend, author__accepter=request.user.id) |
                            Q(visibility=Post.friend, author__requester=request.user.id) |
                            Q(visibility=Post.FOAF, author__requester__requester=request.user.id) |
                            Q(visibility=Post.FOAF, author__requester__accepter=request.user.id) |
                            Q(visibility=Post.FOAF, author__accepter__requester=request.user.id) |
                            Q(visibility=Post.FOAF, author__accepter__accepter=request.user.id)
    )

    # Nested query lookups aren't supported, so we need to make multiple queries :(

    return render(request, 'posts/all.html', {'posts': p})


@login_required
def my_posts(request):
    """AJAX call that returns the user's posts"""
    posts = Post.objects.filter(author__username=request.user.username)
    return render(request, 'posts/all.html', {{'posts': posts}})