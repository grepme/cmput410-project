from django.shortcuts import render, redirect
from user_profile.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from api.models import Server
import json

# Create your views here.


@login_required
def profile(request, guid):
    """Returns a specific author profile"""

    # Get the user's profile. Get is useful for one object.
    # https://docs.djangoproject.com/en/1.7/topics/db/queries/#lookups-that-span-relationships
    profile = None
    try:
        profile = Profile.objects.get(guid=guid)
    except Profile.DoesNotExist as e:
        servers = Server.objects.all()
        for server in servers:
            profile = server.get_author_id(guid)
            if profile is not None:
                profile["is_external"] = True
                break;
        return render(request, "profile/author.html", {'author_profile': request.profile, 'profile': profile})
    # TODO: Return profile not found if that's the case
    profile_dict = profile.as_dict()
    profile_dict["is_external"] = profile.is_external
    return render(request, "profile/author.html", {'author_profile': request.profile, 'profile': profile_dict})

@login_required
def user_profile(request):
    """This will redirect /profile/ to /profile/<profile.guid>"""
    return redirect(profile, request.profile.guid)


@login_required()
def update_profile(request):
    """This will update all posted fields"""


    # Allowed fields the user can update
    allowed_field = ['display_name', 'github_name']

    # Profile object to save
    user = Profile.objects.get(guid=request.profile.guid)

    # Iterate over all posted fields in profile update
    for key, value in request.POST.items():
        if key in allowed_field:
            setattr(user, key, value)
    # Images are in a dictionary that were encoded in the multipart
    if "upload_image" in request.FILES:
        image = request.FILES['upload_image']
        setattr(user, 'image', image)
    else:

    user.save()

    return HttpResponse(json.dumps({'status': True}), content_type='application/json')

@login_required()
def update_profilepic(request):
    """This will update all posted fields"""
    # Profile object to save
    user = Profile.objects.get(guid=request.profile.guid)

    # Images are in a dictionary that were encoded in the multipart
    if "upload_image" in request.FILES:
        image = request.FILES['upload_image']
        setattr(user, 'image', image)
    else:

    user.save()


    return redirect('/profile/')
