from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_protect

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


@login_required
def dashboard(request):
    """The dashboard contains all required information for the social network."""
    return render(request, 'framework/dashboard.html')


@login_required()
def logout(request):
    """Log the user out and redirect to login page."""
    django_logout(request)
    return redirect(login)