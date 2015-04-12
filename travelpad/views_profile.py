from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
from travelpad.forms_profile import *
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse

def get_travelpaduser(id):
	user = get_object_or_404(TravelPadUser, id=id)
	if not user:
		print "get_travelpaduser(" + id + ") not found"
		raise Http404
	return user

@login_required
def profile(request):
	travelpaduser = get_travelpaduser(request.user.id)
	travelpaduser_form = TravelPadUserForm(instance = travelpaduser)
	travelpaduser_form.fields["first_name"].initial = request.user.first_name
	travelpaduser_form.fields["last_name"].initial = request.user.last_name
	travelpaduser_form.fields["email"].initial = request.user.email

	context = {}
	context["travelpaduser_form"] = travelpaduser_form
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
	request.user.first_name = request.POST['first_name']
	request.user.last_name = request.POST['last_name']
	request.user.email = request.POST['email']
	request.user.save()
	travelpaduser = get_travelpaduser(request.user.id)
	if "photo-clear" in request.POST:
		travelpaduser.photo = None
		user_form = TravelPadUserForm(request.POST, instance = travelpaduser)
	elif request.FILES:
		user_form = TravelPadUserForm(request.POST, request.FILES, instance = travelpaduser)
	else:
		user_form = TravelPadUserFormWithoutPhoto(request.POST, instance = travelpaduser)
	if not user_form.is_valid():
		print "update_profile user_form.is_valid fail"
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
	travelpaduser = get_travelpaduser(id)
	if not travelpaduser.photo:
		print "travelpaduser[" + id + "].photo not found"
		raise Http404
	return HttpResponse(travelpaduser.photo, content_type="image")
