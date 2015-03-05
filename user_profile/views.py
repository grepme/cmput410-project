from django.shortcuts import render, redirect
from user_profile.models import Profile
from django.contrib.auth.models import User

# Create your views here.


def profile(request, author):
    """Returns a specific author profile"""

    # Get the user's profile. Get is useful for one object.
    # https://docs.djangoproject.com/en/1.7/topics/db/queries/#lookups-that-span-relationships
    p = Profile.objects.get(author__username=author)
    return render(request, "profile/author.html", {'profile': p})


def user_profile(request):
    """This will redirect /profile/ to /profile/<username>"""
    return redirect(profile, request.user.username)