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

        text = request.POST.get("text", "")

        # Images are in a dictionary that were encoded in the multipart
        if "upload_image" in request.FILES:
            image = request.FILES['upload_image']
        else:
            image = None
        # TODO : Don't rely on post title!
        post_title = request.POST.get("post", "")
        p = Post.objects.get(title=post_title)

        # Fetch the user that uploaded this
        a = User.objects.get(username=request.user.username)

        # Make the comment object
        c = Comment.objects.create(date=timezone.now(), text=text, image=image, post=p, author=a)
        c.save()
        print("Saved")
        print(c)

        # Since this is a view, redirect successfully
        return redirect('/dashboard/')
    else:
        # Accept only POST, otherwise, redirect
        return redirect('/')

@login_required
def posts_comments(request):
    print("You Got To Me")
    # if request.method == 'GET':
    """AJAX call that will grab all comments belonging to a post."""
    print(request)
    # TODO: Add all filters
    # c = Comment.objects.filter(Q(text="justAtest"))
    c = Comment.objects.all()
    print c[0]


    return render(request, 'comments/post.html', {'comments': c})