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

@login_required
def debug_database(request):
	logger.debug("debug_database")
	context = {}
	context['itineraries'] = Itinerary.objects.all()
	itinerary = Itinerary()
	if request.method == "GET":
		itinerary_form = DebugItineraryForm(instance = itinerary)
	else:
		itinerary_form = DebugItineraryForm(request.POST, instance = itinerary)
	context['itinerary_form'] = itinerary_form
	return render(request, 'travelpad/debug.html', context)
	
@login_required
def debug_get_itinerary_photo(request, id):
	logger.debug("debug_get_itinerary_photo(" + id + ")")
	# itinerary = get_object_or_404(Itinerary, id=id)
	itinerary = get_itinerary(id)
	if not itinerary:
		logger.warn("itinerary with id=" + id + " not found")
		raise Http404
	if not itinerary.photo:
		logger.warn("itinerary[" + id + "].photo not found")
		raise Http404
	return HttpResponse(itinerary.photo, content_type="image")
	
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
def debug_delete_itinerary_photo(request):
	logger.debug("debug_delete_itinerary_photo")
	if request.method == "GET":
		logger.warn("debug_delete_itinerary_photo POST only")
		return debug_database(request)
	if not "id" in request.POST:
		logger.warn("debug_delete_itinerary_photo not id in request.POST")
		return debug_database(request)
	id = request.POST["id"]
	itinerary = get_itinerary(id)
	itinerary.photo = None
	itinerary.save()
	return redirect("debug_database")
	