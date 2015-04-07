from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
from travelpad.forms_itineraries import *
from travelpad.views_itinerary import demo
from django.contrib.auth.decorators import login_required

def get_itinerary(id):
	itinerary = get_object_or_404(Itinerary, id=id)
	if not itinerary:
		logger.warn("get_itinerary(" + id + ") not found")
		raise Http404
	return itinerary

@login_required
def itineraries(request):
	context = {}
	# todo created_by
	context["itineraries"] = Itinerary.objects.filter(participants=request.user)
	return render(request, 'travelpad/itineraries.html', context)

@login_required
def add_itinerary_page(request):
	context = {}
	itinerary = Itinerary()
	itinerary_form = ItineraryForm(instance = itinerary)
	context = {}
	context["itinerary_form"] = itinerary_form
	return render(request, 'travelpad/add_itinerary_page.html', context)

@login_required
def update_itinerary_page(request, id):
	context = {}
	itinerary = get_itinerary(id)
	itinerary_form = ItineraryForm(instance = itinerary)
	context = {}
	context["itinerary_id"] = id
	context["itinerary_form"] = itinerary_form
	return render(request, 'travelpad/update_itinerary_page.html', context)

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
		print itinerary_form.errors
		return redirect("itineraries")
	itinerary_form.save()
	return redirect("itineraries")

@login_required
@transaction.atomic
def update_itinerary(request, id):
	if request.method == "GET":
		print "update_itinerary POST only"
		return redirect("itineraries")
	itinerary = get_itinerary(id)
	if not request.FILES:
		itinerary.photo = None
	itinerary_form = ItineraryForm(request.POST, request.FILES, instance = itinerary)
	if not itinerary_form.is_valid():
		print "debug_add_itinerary form.is_valid fail"
		print itinerary_form.errors
		return redirect("itineraries")
	itinerary_form.save()
	return redirect("itineraries")

def itinerary(request, id):
	return redirect("default")