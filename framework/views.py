from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from posts.models import Post
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
        print(firstName,lastName,email,username,password)

        if User.objects.filter(username=username).exists():
            # try to log in as this user
            user = authenticate(username=username, password=password)
            if user is not None:
                # password already matches username
                if user.is_active:
                    django_login(request, user)
                    return redirect(dashboard)
            else:
                print("Username already in use: %s" % username)
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

@login_required
def dashboard(request):
    """The dashboard contains all required information for the social network."""
    # Grab the user's stream (needs to be updated)
    # TODO: Is the stream only their posts?
    posts = Post.objects.filter(author=request.profile)

    # TODO: Time stamps need to be standardized and formatted.
    # TODO: Limit them to 5?
    github_feed = {}
    if request.profile.github_name is not None:
        github_feed = feedparser.parse("https://github.com/{}.atom".format(request.profile.github_name))
    return render(request, 'framework/dashboard.html', {'posts': posts, 'github_feed': github_feed})


@login_required()
def logout(request):
    """Log the user out and redirect to login page."""
    django_logout(request)
    return redirect(login)
