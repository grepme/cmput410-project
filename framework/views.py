from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.


def login(request):
    """If user is logged in, redirect to dashboard, else, render login template."""
    if request.user.is_authenticated():
        return redirect(dashboard)
    else:
        return render(request, 'framework/login.html')


@login_required
def dashboard(request):
    """The dashboard contains all required information for the social network."""
    return render(request, 'framework/dashboard.html')
