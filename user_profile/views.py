from django.shortcuts import render, redirect

# Create your views here.


def profile(request, username=None):
    """Returns a specific author profile"""
    if not username:
        return redirect("/")
    else:
        return render(request, "profile/author.html")


def user_profile(request):
    """This will redirect /profile/ to /profile/<username>"""
    return redirect(profile, author=request.user.username)