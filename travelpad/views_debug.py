from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
from travelpad.forms_debug import *
from travelpad.views_itinerary import demo
import logging
import sys

logger = logging.getLogger('debug')
hdlr = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

def get_itinerary(id):
	itinerary = get_object_or_404(Itinerary, id=id)
	if not itinerary:
		logger.warn("get_itinerary(" + id + ") not found")
		raise Http404
	return itinerary

def get_travelpaduser(id):
	travelpaduser = get_object_or_404(TravelPadUser, id=id)
	if not travelpaduser:
		logger.warn("get_travelpaduser(" + id + ") not found")
		raise Http404
	return travelpaduser
	
@login_required
def debug_database(request):
	logger.debug("debug_database")
	context = {}
	context['itineraries'] = Itinerary.objects.all()
	itinerary = Itinerary()
	itinerary_form = DebugItineraryForm(request.POST, instance = itinerary)
	context['itinerary_form'] = itinerary_form
	context['travelpadusers'] = TravelPadUser.objects.all()
	travelpaduser = TravelPadUser()
	travelpaduser_form = DebugTravelPadUserForm(request.POST, instance = travelpaduser)
	context['travelpaduser_form'] = travelpaduser_form
	return render(request, 'travelpad/debug.html', context)
	
@login_required
def debug_get_itinerary_photo(request, id):
	logger.debug("debug_get_itinerary_photo(" + id + ")")
	itinerary = get_itinerary(id)
	if not itinerary:
		logger.warn("itinerary with id=" + id + " not found")
		raise Http404
	if not itinerary.photo:
		logger.warn("itinerary[" + id + "].photo not found")
		raise Http404
	return HttpResponse(itinerary.photo, content_type="image")

@login_required
def debug_get_travelpaduser_photo(request, id):
	logger.debug("debug_get_travelpad_photo(" + id + ")")
	travelpaduser = get_travelpaduser(id)
	if not travelpaduser:
		logger.warn("travelpaduser with id=" + id + " not found")
		raise Http404
	if not travelpaduser.photo:
		logger.warn("travelpaduser[" + id + "].photo not found")
		raise Http404
	return HttpResponse(travelpaduser.photo, content_type="image")
	
@login_required
@transaction.atomic
def debug_add_itinerary(request):
	logger.debug("debug_add_itinerary")
	if request.method == "GET":
		logger.warn("debug_add_itinerary POST only")
		return debug_database(request)	
	itinerary = Itinerary()
	if "exist_id" in request.POST:
		id = request.POST["exist_id"]
		if id:
			itinerary = get_itinerary(id)
	if not request.FILES:
		itinerary.photo = None
	itinerary_form = DebugItineraryForm(request.POST, request.FILES, instance = itinerary)
	if not itinerary_form.is_valid():
		print itinerary_form.errors
		logger.warn("debug_add_itinerary form.is_valid fail")
		return debug_database(request)
	itinerary_form.save()
	return redirect("debug_database")

@login_required
@transaction.atomic
def debug_delete_itinerary(request):
	logger.debug("debug_delete_itinerary")
	if request.method == "GET":
		logger.warn("debug_delete_itinerary POST only")
		return debug_database(request)
	if not "id" in request.POST:
		logger.warn("debug_delete_itinerary not id in request.POST")
		return debug_database(request)
	id = request.POST["id"]
	itinerary = get_itinerary(id)
	itinerary.delete()
	return redirect("debug_database")

@login_required
@transaction.atomic
def debug_add_travelpaduser(request):
	logger.debug("debug_add_travelpaduser")
	if request.method == "GET":
		logger.warn("debug_add_travelpaduser POST only")
		return debug_database(request)
	travelpaduser = TravelPadUser()
	if "exist_id" in request.POST:
		id = request.POST["exist_id"]
		if id:
			travelpaduser = get_travelpaduser(id)
	if not request.FILES:
		travelpaduser.photo = None
	travelpaduser_form = DebugTravelPadUserForm(request.POST, request.FILES, instance = travelpaduser)
	if not travelpaduser_form.is_valid():
		print travelpaduser_form.errors
		logger.warn("debug_add_travelpaduser form.is_valid fail")
		return debug_database(request)
	travelpaduser_form.save()
	return redirect("debug_database")
