from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from posts.models import Post
from user_profile.models import Profile
from django.core.validators import validate_email
from django import forms

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
        username = request.POST.get("signupUsername", "")
        password = request.POST.get("signupPassword", "")
        retypedPass = request.POST.get("signupDuplicatePassword", "")
        email = request.POST.get("signupEmail", "")
        print(firstName,lastName,email,username,password)

        if password != retypedPass:
            print("Passwords did not match")
            #TODO: Return validation failed

        if (not firstName) or (not lastName) or (not username) or (not password) or (not retypedPass) or (not email):
            print("Blank field detected")
            #TODO: Return validation failed

        try:
            validate_email(email)
        except forms.ValidationError:
            print("Validation failed")
            #TODO: Return validation failed


        if User.objects.filter(username=username).exists():
            #TODO: Alert user that this is wrong... don't just log in anyway
            # try to log in as this user
            user = authenticate(username=username, password=password)
            if user is not None:
                # # password already matches username
                print("Would you like to login %s?" % user)
                # if user.is_active:
                #     django_login(request, user)
                #     return redirect(dashboard)
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
    return render(request, 'framework/signup.html', {'body_class': 'login-page', 'nav_bar': False})

@login_required
def dashboard(request):
    """The dashboard contains all required information for the social network."""
    # Grab the user's stream (needs to be updated)
    # TODO: Is the stream only their posts?
    posts = Post.objects.filter(author__username=request.user.username)
    # posts = Post.objects.filter(author=request.profile)
    return render(request, 'framework/dashboard.html', {'posts': posts})


@login_required()
def logout(request):
    """Log the user out and redirect to login page."""
    django_logout(request)
    return redirect(login)
