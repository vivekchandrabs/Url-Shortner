from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from shortner.models import UrlTable

import hashlib

# Create your views here.
def _createHash(key):
	hash=hashlib.md5(key)
	return hash.hexdigest()[:6]

def signup(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		email = request.POST.get("email")

		user = User.objects.create_user(
				username=username,
				password=password,
				email=email
			)
		login(request, user)

		return redirect("/dashboard/")

	return render(request, "signup.html")

def signin(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(username=username, password=password)

		if user != None:
			login(request, user)
			return redirect("/dashboard/")

	return render(request, "signin.html")


def dashboard(request):
	user = request.user
	url_instances = UrlTable.objects.filter(user=user)
	return render(request, "dashboard.html", {"url_instances":url_instances})


def create_short_url(request):
	if request.method == "POST":
		long_url = request.POST.get("long_url")
		title = request.POST.get("title")
		
		user = request.user

		short_hash = _createHash(long_url.encode('utf-8'))

		url = UrlTable.objects.create(
				long_url=long_url, 
				user=user,
				short_hash=short_hash,
				title=title
			)

		return redirect("/dashboard/")



def redirect_to_long_url(request, hashcode):
	
	try:
		url = UrlTable.objects.get(short_hash=hashcode)

		long_url = url.long_url

		url.no_clicks += 1
		url.save()
		
		return redirect(long_url)

	except:
		return HttpResponse("URL Not Found")

def signout(request):
	logout(request)
	return redirect("/signin/")