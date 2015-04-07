from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
from travelpad.views_itinerary import demo

@login_required
def itinerary_collection(request):
	
	return render(request, 'travelpad/itinerary_collection.html', context)
