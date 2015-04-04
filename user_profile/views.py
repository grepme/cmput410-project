from django.shortcuts import render, redirect
from user_profile.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

# Create your views here.


@login_required
def profile(request, author):
    """Returns a specific author profile"""

    # Get the user's profile. Get is useful for one object.
    # https://docs.djangoproject.com/en/1.7/topics/db/queries/#lookups-that-span-relationships
    profile = Profile.objects.filter(display_name=author).first()
    if profile is not None:
        return render(request, "profile/author.html", {'profile': profile})
    # TODO: Return profile not found if that's the case
    return render(request, "profile/author.html", {'profile': request.profile})

@login_required
def user_profile(request):
    """This will redirect /profile/ to /profile/<username>"""
    return redirect(profile, request.user.username)


@login_required()
def update_profile(request):
    """This will update all posted fields"""


    # Allowed fields the user can update
    allowed_field = ['display_name', 'github_name']

    # Profile object to save
    user = Profile.objects.get(guid=request.profile.guid)

    # Iterate over all posted fields in profile update
    for key, value in request.POST.items():
        print key + " // " + value
        if key in allowed_field:
            setattr(user, key, value)
    user.save()
    print user.github_name

    return HttpResponse(json.dumps({'status': True}), content_type='application/json')
