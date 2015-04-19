from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
from travelpad.forms_itineraries import *
from travelpad.views_itinerary import demo
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse

def get_itinerary(id):
	itinerary = get_object_or_404(Itinerary, id=id)
	if not itinerary:
		print "get_itinerary(" + id + ") not found"
		raise Http404
	return itinerary

@login_required
def itineraries(request):
	context = {}
	# todo created_by
	context["itineraries"] = Itinerary.objects.filter(participants=request.user)
	context["itinerary_form"] = ItineraryForm()
	return render(request, 'travelpad/itineraries.html', context)

@login_required
def get_itineraryform_json(request, id):
	itinerary = Itinerary.objects.filter(id=id)
	response_text = serializers.serialize('json', itinerary)
	return HttpResponse(response_text, content_type='application/json')
	
@login_required
@transaction.atomic
def add_itinerary(request):
	if request.method == "GET":
		print "add_itinerary POST only"
		return redirect("itineraries")
	itinerary = Itinerary()
	itinerary.created_by = request.user
	if not request.FILES:
		itinerary.photo = None
	itinerary_form = ItineraryForm(request.POST, request.FILES, instance = itinerary)
	if not itinerary_form.is_valid():
		print "debug_add_itinerary form.is_valid fail"
		response_text = serializers.serialize('json', itinerary_form.errors)
		return HttpResponse(response_text, content_type='application/json')
	itinerary_form.save()
	return redirect("itineraries")

@login_required
@transaction.atomic
def update_itinerary(request, id):
	if request.method == "GET":
		print "update_itinerary POST only"
		return redirect("itineraries")
	if id == "0":
		itinerary = Itinerary(created_by=request.user)
	else:
		itinerary = get_itinerary(id)
	print "request.POST = ", request.POST
	if request.POST.get("clear"):
		itinerary.photo = None
	if not request.FILES:
		itinerary_form = ItineraryFormWithoutPhoto(request.POST, instance = itinerary)
	else:
		itinerary_form = ItineraryForm(request.POST, request.FILES, instance = itinerary)
	if not itinerary_form.is_valid():
		print "update_itinerary form.is_valid fail"
		response_text = serializers.serialize('json', itinerary_form.errors)
		return HttpResponse(response_text, content_type='application/json')
	itinerary_form.save()
	if id == "0":
		itinerary.participants.add(User.objects.get(id=request.user.id))
		itinerary.save()
	return redirect("itineraries")

@login_required
@transaction.atomic
def delete_itinerary(request):
	if request.method == "GET":
		print "delete_itinerary POST only"
		return redirect("itineraries")
	if not "id" in request.POST:
		print "no id in request.POST"
		return redirect("itineraries")
	itinerary = get_itinerary(request.POST["id"])
	itinerary.delete()
	return redirect("itineraries")

@login_required
def get_itinerary_photo(request, id):
	itinerary = get_itinerary(id)
	if not itinerary.photo:
		print "itinerary[" + id + "].photo not found"
		raise Http404
	return HttpResponse(itinerary.photo, content_type="image")
