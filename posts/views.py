from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from posts.models import Post

# Create your views here


@login_required
def new_post(request):
    if request.method == 'POST':
        format = request.POST.get("content_type", "")
        visibility = request.POST.get("visibility", "")
        text = request.POST.get("text", "")
        # p = Post.objects.get_or_create(title="???", date=datetime.now(), text=text, image = ???, origin = ???, source = ???,author=, visibility=visibility)[0]

    return render(request, 'framework/dashboard.html')

