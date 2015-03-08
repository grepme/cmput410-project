from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_protect

from Post.models import Post

def new_post (request){
	if request.methof == 'POST':
		format = request.POST.get("content_type","")
		visibility = request.POST.get("visibility","")
		text = request.POST.get("text", "")
		#p = Post.objects.get_or_create(title="???", date=datetime.now(), text=text, image = ???, origin = ???, source = ???,author=, visibility=visibility)[0]
		
	return return render(request, 'framework/dashboard.html')
}
# Create your views here.
