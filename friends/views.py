from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from friends.models import Friend, Follow
from django.db.models import Q
from user_profile.models import Profile

def get_other_profiles(profile,query):
    profiles = list()

    for query_item in query:
        if query_item.accepter == profile:
            profiles.append(query_item.requester)
        else:
            profiles.append(query_item.accepter)
    return profiles

def get_other_following(profile,query):
    profiles = list()

    for query_item in query:
            profiles.append(query_item.requester)

    return profiles

@login_required
def friends(request):
    return render(request, "friends/index.html", {"user":request.user,"profile":request.profile})

# Create your views here.
@login_required
def friends_friends(request):
    # find all of our friends
    friends_query = Friend.objects.filter(Q(accepter=request.profile,accepted=True) | Q(requester=request.profile,accepted=True))

    friends_profile = get_other_profiles(request.profile,friends_query)

    return render(request, "friends/accepted.html", {'profiles': friends_profile, "user":request.user,"profile":request.profile})

# Create your views here.
@login_required
def following_friends(request):
    # find all of our friends
    follow_query = Follow.objects.filter(Q(follower=request.profile))

    profiles = [item.following for item in follow_query]

    return render(request, "friends/accepted.html", {'profiles': profiles, "user":request.user,"profile":request.profile})

@login_required
def incoming_friends(request):
    # get current friends
    incoming_query = Friend.objects.filter(accepter=request.profile,accepted=False)
    profiles = [item.requester for item in incoming_query]
    return render(request, "friends/incoming.html", {'profiles': profiles, "user":request.user})

@login_required
def sent_friends(request):
    # get current friends
    sent_query = Friend.objects.filter(requester=request.profile,accepted=False)
    profiles = [item.accepter for item in sent_query]
    return render(request, "friends/sent.html", {'profiles': profiles, "user":request.user})

@login_required
def search_friends(request,name):
    search = Profile.objects.filter(Q(display_name__icontains=name) & ~Q(guid=request.profile.guid))
    return render(request, "friends/search.html",{"profiles":search})

@login_required
def search_all(request):
    search = Profile.objects.filter(~Q(guid=request.profile.guid))
    return render(request, "friends/search.html",{"profiles":search})
@login_required
def delete(request, friend_guid):
    nothing_found = True
    friend_profile = Profile.objects.filter(guid=friend_guid).first()
    old_friend = Friend.objects.filter(Q(requester=request.profile, accepter=friend_profile) |
                                       Q(accepter=request.profile, requester=friend_profile)).first()
    if old_friend is not None:
        old_friend.delete()
        nothing_found = False
    old_follow = Follow.objects.filter(Q(following=request.profile, follower=friend_profile) |
                                       Q(follower=request.profile, following=friend_profile)).first()
    if old_follow is not None:
        old_follow.delete()
        nothing_found=False

    if(nothing_found):
        return HttpResponse(404)

    return HttpResponse(200)
