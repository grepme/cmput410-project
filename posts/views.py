from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from posts.models import Post
from django.contrib.auth.models import User

# Create your views here


@login_required
def new_post(request):
    if request.method == 'POST':
        title = request.POST.get("title", "")
        text_format = request.POST.get("content_type", "")
        if text_format == "commonmark":
            text_format = True
        else:
            text_format = False
        visibility = request.POST.get("visibility", "Private")
        visibility = Post.get_visibility(visibility)
        text = request.POST.get("text", "")
        image = request.FILES['upload_image']
        print request.FILES
        a = User.objects.get(username=request.user.username)
        p = Post.objects.create(title=title, date=timezone.now(), text=text, image=image, origin='127.0.0.1',
                                source='127.0.0.1', visibility=visibility, commonmark=text_format, author=a)
        p.save()
        return redirect('/dashboard/')
    else:
        redirect('/')