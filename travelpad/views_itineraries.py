from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
from travelpad.views_itinerary import demo
from django.contrib.auth.decorators import login_required

@login_required
def itineraries(request):
	context = {}
	# todo filter itineraries related to the request.user 
	context["itineraries"] = Itinerary.objects.all()
	return render(request, 'travelpad/itineraries.html', context)

def itinerary(request, id):
	return redirect("default")