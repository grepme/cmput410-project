from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from posts.models import Post
from friends.models import Friend,Follow
from user_profile.models import Profile
import feedparser

# Create your views here.


def login(request):
    """If user is logged in, redirect to dashboard, else, render login template."""
    if request.user.is_authenticated():
        return redirect(dashboard)
    elif request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            # Password is good
            if user.is_active:
                django_login(request, user)
                if request.POST.get("remember-me", None):
                    request.session.set_expiry(0)
                return redirect(dashboard)
    return render(request, 'framework/login.html', {'body_class': 'login-page', 'nav_bar': False})

def signup(request):
    """If user is logged in, redirect to dashboard, else, render login template."""
    if request.user.is_authenticated():
        return redirect(dashboard)
    elif request.method == "POST":
        firstName = request.POST.get("signupFirstName", "")
        lastName = request.POST.get("signupLastName", "")
        email = request.POST.get("signupEmail", "")
        username = request.POST.get("signupUsername", "")
        password = request.POST.get("signupPassword", "")

        if User.objects.filter(username=username).exists():
            # try to log in as this user
            user = authenticate(username=username, password=password)
            if user is not None:
                # password already matches username
                if user.is_active:
                    django_login(request, user)
                    return redirect(dashboard)
            else:
        # username does not yet exist
        else:
            newUser = User.objects.create_user(username=username, email=email, password=password)
            # newUser.save()  # didn't seem to do anything
            if newUser:
                # TODO: Add both names, url, and host (and user.guid?)
                profile = Profile.objects.create(author=newUser, display_name=username)
                # profile = Profile.objects.create(id=newUser.id, display_name=username)
                profile.save()

                user = authenticate(username=username, password=password)
                if user is not None:
                    # creation and login successful
                    if user.is_active:
                        django_login(request, user)
                        return redirect(dashboard)
            else:
                # user creation failed
                pass
    return render(request, 'framework/login.html', {'body_class': 'login-page', 'nav_bar': False})

def get_other_profiles(profile, query):
    profiles = list()

    for query_item in query:
        if query_item.accepter == profile:
            profiles.append(query_item.requester)
        else:
            profiles.append(query_item.accepter)
    return profiles


def get_other_friends(friends, query):
    profiles = list()
    for query_item in query:
        if query_item.accepter in friends:
            profiles.append(query_item.requester)
        else:
            profiles.append(query_item.accepter)
    return profiles

@login_required
def dashboard(request):
    """The dashboard contains all required information for the social network."""
    # Grab the user's stream (needs to be updated)
    # TODO: Is the stream only their posts?

    # All My Posts
    # All Posts of anyone I follow with Public Visibility
    # Any posts of my friends with Visibility Friends and following
    # Any of my Friends that have same server and visibility local friends
    # FOAF - Local and Remote

    # All people I follow
    following = Follow.objects.filter(follower=request.profile)

    # My Friends
    friends = Friend.objects.filter(Q(requester=request.profile) | Q(accepter=request.profile))

    # The Friends Profile
    friends = get_other_profiles(request.profile,friends)

    # Get my Friends of Friends
    friends_friends = Friend.objects.filter(Q(requester__in=friends) | Q(accepter__in=friends))

    # Get the other friends..
    friends_friends = get_other_friends(friends,friends_friends)

    posts = Post.objects.filter(Q(author=request.profile) | Q(author__following__in=following,visibility=Post.public) |
                                Q(visibility=Post.friend, author__accepter=request.profile,author__following__in=following) |
                                Q(visibility=Post.server, author__accepter=request.profile,author__following__in=following) |
                                Q(visibility=Post.friend, author__requester=request.profile,author__following__in=following) |
                                Q(author__in=friends_friends,visibility=Post.FOAF)).distinct()

    # TODO: Time stamps need to be standardized and formatted.
    # TODO: Limit them to 5?
    github_feed = {}
    if request.profile.github_name is not None:
        github_feed = feedparser.parse("https://github.com/{}.atom".format(request.profile.github_name))
    return render(request, 'framework/dashboard.html', {'posts': posts, 'github_feed': github_feed.entries[:10], 'author_profile': request.profile})


@login_required()
def logout(request):
    """Log the user out and redirect to login page."""
    django_logout(request)
    return redirect(login)
