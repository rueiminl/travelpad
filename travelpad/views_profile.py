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
	user = get_object_or_404(User, id=id)
	if not user:
		print "get_travelpaduser(" + id + ") not found"
		raise Http404
	travelpaduser = get_object_or_404(TravelPadUser, user=user)
	if not travelpaduser:
		print "get_travelpaduser(" + id + ") not found"
		raise Http404
	return travelpaduser

@login_required
def profile(request):
	travelpaduser = get_travelpaduser(request.user.id)
	travelpaduser_form = TravelPadUserForm(instance = travelpaduser)
	travelpaduser_form.fields["first_name"].initial = request.user.first_name
	travelpaduser_form.fields["last_name"].initial = request.user.last_name
	travelpaduser_form.fields["email"].initial = request.user.email

	itineraries = Itinerary.objects.filter(participants__id=request.user.id)
	todoes = Todo.objects.filter(owner__id=request.user.id)
	
	context = {}
	if 'errors' in request.session:
		context["errors"] = request.session["errors"]
		del request.session["errors"]	
	context["travelpaduser_form"] = travelpaduser_form
	context["itineraries"] = itineraries
	context["todoes"] = todoes
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
	travelpaduser = get_travelpaduser(request.user.id)
	if request.POST.get("clear"):
		travelpaduser.photo = None
		user_form = TravelPadUserFormWithoutPhoto(request.POST, instance = travelpaduser)
	elif request.FILES:
		user_form = TravelPadUserForm(request.POST, request.FILES, instance = travelpaduser)
	else:
		user_form = TravelPadUserFormWithoutPhoto(request.POST, instance = travelpaduser)
	if not user_form.is_valid():
		print "update_profile user_form.is_valid fail"
		print user_form.errors
		request.session["errors"] = [k + ":" + v[0] for k, v in user_form.errors.items()]
		return redirect("profile")
	user_form.save()
	request.user.first_name = request.POST['first_name']
	request.user.last_name = request.POST['last_name']
	request.user.email = request.POST['email']
	request.user.save()
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
		return redirect("/static/travelpad/img/DefaultPersonPhoto.png")
	return HttpResponse(travelpaduser.photo, content_type="image")
