from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from comments.models import Comment
from django.contrib.auth.models import User
from posts.models import Post
from django.db.models import Q
from friends.models import Friend


@login_required
def new_comment(request, source=None):
    if request.method == 'POST':

        # Text from the context of the comment
        text = request.POST.get("text", "")

        # Images are in a dictionary that were encoded in the multipart
        if "upload_image" in request.FILES:
            image = request.FILES['upload_image']
        else:
            image = None
        post_id = request.POST.get("post_id", "")
        p = Post.objects.get(guid=post_id)

        # Fetch the user that uploaded this
        a = request.profile

        # Make the comment object
        c = Comment.objects.create(date=timezone.now(), text=text, image=image, post=p, author=a)
        c.save()

        # Since this is a view, redirect successfully
        return redirect('/dashboard/')
    else:
        # Accept only POST, otherwise, redirect
        return redirect('/')
