from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
import json
from travelpad.models import *

def save_place(request):
	if not 'coordinate' in request.POST or not request.POST['coordinate']:
		print "No Post item"
		return render(request, 'travelpad/index.html')
	s = request.POST['coordinate'][1:-1]
	tmp = s.split(', ')
	place_id = request.POST['placeId']
	try:
		Event.objects.get(place_id=place_id)
		print "Already exist"
	except Event.DoesNotExist:
		new_place = Event.objects.create(place_latitude=tmp[0],
										 place_longitude=tmp[1],
										 place_id=place_id,)
		new_place.save()
		print "New Item"
	places = Event.objects.all()
	#places = [obj.get_json() for obj in Place.objects.all()]
	#context = json.dumps({'lat': tmp[0], 'lng': tmp[1], 'placeId': request.POST['placeId'], 'places': places})
	context = {'lat': tmp[0], 'lng': tmp[1], 'placeId': request.POST['placeId'], 'places': places}
	return render(request, 'travelpad/index.html', context)
def add_place(request):
	return render(request, 'travelpad/search.html')