from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from posts.models import Post
from django.contrib.auth.models import User

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