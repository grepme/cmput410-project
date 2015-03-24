from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from friends.models import Friend, Follow
from django.db.models import Q
from user_profile.models import Profile

@login_required
def friends(request):
    profile = Profile.objects.get(author=request.user)
    return render(request, "friends/index.html", {"user":request.user,"profile":profile})

# Create your views here.
@login_required
def friends_friends(request):
    # find all of our friends
    friends_query = Friend.objects.filter(Q(accepter=request.user,accepted=True) | Q(requester=request.user,accepted=True))

    # Get all profiles for accepter and requester
    # Don't include ourselves
    friends_profile = Profile.objects.filter((Q(author__in=[friend.requester for friend in friends_query]) | Q(author__in=[friend.accepter for friend in friends_query])) & ~Q(author=request.user))
    profile = Profile.objects.get(author=request.user)
    return render(request, "friends/accepted.html", {'profiles': friends_profile, "user":request.user,"profile":profile})

# Create your views here.
@login_required
def following_friends(request):
    # find all of our friends
    follow_query = Follow.objects.filter(Q(follower=request.user))

    print follow_query
    print [follow.following for follow in follow_query]

    # Get all profiles for accepter and requester
    # Don't include ourselves
    friends_profile = Profile.objects.filter(Q(author__in=[follow.following for follow in follow_query]))
    profile = Profile.objects.get(author=request.user)
    return render(request, "friends/accepted.html", {'profiles': friends_profile, "user":request.user,"profile":profile})

@login_required
def incoming_friends(request):
    # get current friends
    friends_query = Friend.objects.filter(accepter=request.user.id,accepted=False)
    sent_query = Profile.objects.filter(author__in=[friend.requester for friend in friends_query])
    return render(request, "friends/request.html", {'profiles': sent_query, "user":request.user})

@login_required
def sent_friends(request):
    # get current friends
    friends_query = Friend.objects.filter(requester=request.user.id,accepted=False)
    sent_query = Profile.objects.filter(author__in=[friend.accepter for friend in friends_query])
    return render(request, "friends/request.html", {'profiles': sent_query, "user":request.user})



@login_required
def search_friends(request,name):
    search = Profile.objects.filter(Q(display_name__icontains=name) & ~Q(author=request.user))
    return render(request, "friends/search.html",{"profiles":search})


