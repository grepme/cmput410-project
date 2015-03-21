from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from friends.models import Friend, Follow
from django.db.models import Q

# Create your views here.
@login_required
def friends(request):
    friends_query = Friend.objects.filter(Q(accepter=request.user.id,accepted=True) | Q(requester=request.user.id,accepted=True))
    return render(request, "friends/friends.html", {'friends': friends_query})

@login_required
def search_friends(request):
    return render(request, "friends/search.html")


