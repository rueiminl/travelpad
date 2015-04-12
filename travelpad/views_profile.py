from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
from travelpad.forms_profile import *
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse

def get_user(id):
	user = get_object_or_404(TravelPadUser, id=id)
	if not user:
		print "get_user(" + id + ") not found"
		raise Http404
	return user

@login_required
def profile(request):
	context = {}
	context["user_form"] = UserForm()
	context["travelpaduser_form"] = TravelPadUserForm()
	return render(request, 'travelpad/profile.html', context)

@login_required
def get_userform_json(request, id):
	user = TravelPadUser.objects.filter(id=id)
	response_text = serializers.serialize('json', user)
	return HttpResponse(response_text, content_type='application/json')
	
@login_required
@transaction.atomic
def update_profile(request):
	if request.method == "GET":
		print "update_user POST only"
		return redirect("profile")
	user = TravelPadUser.objects.get(user=request.user)
	if request.POST.get("clear"):
		user.photo = None
	if not request.FILES:
		user_form = TravelPadUserFormWithoutPhoto(request.POST, instance = user)
	else:
		user_form = TravelPadUserForm(request.POST, request.FILES, instance = user)
	if not user_form.is_valid():
		print "update_user form.is_valid fail"
		print user_form.errors
		return redirect("profile")
	user_form.save()
	return redirect("profile")

@login_required
@transaction.atomic
def delete_user(request):
	if request.method == "GET":
		print "delete_user POST only"
		return redirect("profile")
	user = TravelPadUser.objects.get(user=request.user)
	user.delete()
	return redirect("default")

@login_required
def get_user_photo(request, id):
	user = get_user(id)
	if not user.photo:
		print "user[" + id + "].photo not found"
		raise Http404
	return HttpResponse(user.photo, content_type="image")
