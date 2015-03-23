from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *

def calendar(request):
	context = {}
    #TODO: get itenarary and events
    
	return render(request, 'travelpad/calendar.html', context)

