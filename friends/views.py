from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from friends.models import Friend, Follow, FriendRequest
from django.db.models import Q
from django.db import IntegrityError
from user_profile.models import Profile
from api.models import Server
from urlparse import urlparse

import json

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
    return render(request, "friends/index.html", {"user":request.user,"author_profile":request.profile})

# Create your views here.
@login_required
def friends_friends(request):
    # find all of our friends
    friends_query = Friend.objects.filter(Q(accepter=request.profile) | Q(requester=request.profile))

    friends_profile = get_other_profiles(request.profile,friends_query)

    return render(request, "friends/accepted.html", {'profiles': friends_profile, "user":request.user,"author_profile":request.profile,"type": "friends"})

# Create your views here.
@login_required
def following_friends(request):
    # find all of our friends
    follow_query = Follow.objects.filter(Q(follower=request.profile))

    profiles = [item.following for item in follow_query]

    return render(request, "friends/accepted.html", {'profiles': profiles, "user":request.user,"author_profile":request.profile,"type": "following"})

@login_required
def incoming_friends(request):
    # get current friends
    incoming_query = FriendRequest.objects.filter(accepter=request.profile)
    profiles = [item.requester for item in incoming_query]
    return render(request, "friends/request.html", {'profiles': profiles, "user":request.user, "direction": "incoming"})

@login_required
def sent_friends(request):
    # get current friends
    sent_query = FriendRequest.objects.filter(requester=request.profile)
    profiles = [item.accepter for item in sent_query]
    return render(request, "friends/request.html", {'profiles': profiles, "user":request.user, "direction": "sent"})

@login_required
def search_friends(request,name):
    search = Profile.objects.filter(Q(display_name__icontains=name) & ~Q(guid=request.profile.guid) & Q(is_external=False))
    return render(request, "friends/search.html",{"profiles":search})

@login_required
def search_all(request):
    search = Profile.objects.filter(~Q(guid=request.profile.guid) & Q(is_external=False))
    return render(request, "friends/search.html",{"profiles":search,"author_profile":request.profile})

@login_required
def delete(request, friend_guid):
    nothing_found = True
    friend_profile = Profile.objects.filter(guid=friend_guid).first()
    old_friend = Friend.objects.filter(Q(requester=request.profile, accepter=friend_profile) |
                                       Q(accepter=request.profile, requester=friend_profile)).first()

    old_friend_request = FriendRequest.objects.filter(Q(requester=request.profile, accepter=friend_profile) |
                                       Q(accepter=request.profile, requester=friend_profile)).first()


    if old_friend is not None:
        old_friend.delete()
        nothing_found = False

    if old_friend_request is not None:
        old_friend_request.delete()
        nothing_found = False

    old_follow = Follow.objects.filter(Q(follower=request.profile, following=friend_profile)).first()
    if old_follow is not None:
        old_follow.delete()
        nothing_found=False

    if(nothing_found):
        return HttpResponse(404)

    return HttpResponse(200)

def has_keys(keys, dictionary, main_key):
    for key in keys:
        item = dictionary[main_key]
        if key in item and len(item[key]) > 2:
            continue;
        else:
            return False
    return True

def follow_user(request):
    data = None
    try:
        data = json.loads(request.body)
    except ValueError as e:
        return HttpResponseBadRequest()

    following_guid = data["follow"]["id"]

    # Valid Profile?
    following = None
    try:
        following = Profile.objects.get(guid=following_guid)
    except Profile.DoesNotExist as e:
        res = HttpResponse("Profile with id {} does not exist".format(following_guid))
        res.status_code = 404
        return res

    # Create follow if does not exist
    try:
        Follow.objects.get(follower=request.profile, following=following)
    except Follow.DoesNotExist as e:
        Follow.objects.create(follower=request.profile, following=following)

    # Return 201
    res = HttpResponse()
    res.status_code = 201
    return res

def friend_request(request, page="0"):
    # get data from request
    data = None

    try:
        data = json.loads(request.body)
    except ValueError as e:
        return HttpResponseBadRequest()

    keys = ['id', 'host', 'url', 'displayname']

    if has_keys(keys, data, 'author') and has_keys(keys, data, 'friend'):
        author = Profile.objects.filter(guid=data["author"]["id"]).first()
        friend = Profile.objects.filter(guid=data["friend"]["id"]).first()

        try:
            if author == None:
                author = Profile.objects.create(is_external=True, display_name=data["author"]["displayname"],
                                                host=data["author"]["host"],guid=data["author"]["id"])

            if friend == None:
                friend = Profile.objects.create(is_external=True, display_name=data["friend"]["displayname"],
                                                host=data["friend"]["host"],guid=data["friend"]["id"])

            if author == friend:
                return HttpResponseBadRequest()
        except Exception as e:
            return HttpResponseBadRequest()

        # They Sent us a request First
        found = FriendRequest.objects.filter(Q(accepter=author,requester=friend)).first()

        # Check to make sure we don't have a friend obj already
        found_friend = Friend.objects.filter(Q(requester=friend, accepter=author) | Q(accepter=friend,requester=author)).first()

        # found friendrequest
        if found is not None:

            # Remove Request
            found.delete()
            if found_friend is None:

                # Create Friend Object
                Friend.objects.create(requester=author,accepter=friend)
                send_external_friend_request(author,friend)

                # Add the follow object catch an errors they may be following already
                try:
                    Follow.objects.create(follower=author, following=friend)
                except IntegrityError as e:
                    pass
            return HttpResponse()
        elif found_friend is None:
            # No friend object already create a request
            try:
                FriendRequest.objects.create(requester=author, accepter=friend)
                send_external_friend_request(author,friend)
                Follow.objects.create(follower=author, following=friend)
            except IntegrityError as e:
                pass
            # TODO: return 201?
            return HttpResponse()
        else:
            return HttpResponse()

    return HttpResponseBadRequest()

def send_external_friend_request(author,friend):
    if friend.is_external:
        url = urlparse(friend.host)
        server = Server.objects.filter(host__icontains=url.netloc).first()
        if server is not None:
            return server.post_friend_request(author,friend)


