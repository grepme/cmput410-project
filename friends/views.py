from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from friends.models import Friend, Follow
from django.db.models import Q
from user_profile.models import Profile

# Create your views here.
@login_required
def friends(request):
    friends_query = Friend.objects.filter(Q(accepter=request.user.id,accepted=True) | Q(requester=request.user.id,accepted=True))
    profile = Profile.objects.get(author=request.user)
    return render(request, "friends/index.html", {'friends': friends_query, "user":request.user,"profile":profile})

@login_required
def sent_friends(request):
    friends_query = Friend.objects.filter(requester=request.user,accepted=False)
    sent_query = Profile.objects.filter(author__in=friends_query)
    return render(request, "friends/sent.html", {'sent': sent_query, "user":request.user})



@login_required
def search_friends(request,name):
    search = Profile.objects.filter(display_name__icontains=name)
    return render(request, "friends/search.html",{"profiles":search})


