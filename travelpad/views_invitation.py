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

def get_itinerary_id_by_session(request):
	if not 'itinerary_id' in request.session:
		print "get_itinerary_id_by_session not found itinerary_id"
		raise Http404
	return request.session['itinerary_id']
	
def get_itinerary_by_session(request):
	itinerary_id = get_itinerary_id_by_session(request)
	itinerary = get_object_or_404(Itinerary, id=itinerary_id)
	if not itinerary:
		print "get_itinerary_by_session(" + itinerary_id + ") not found"
		raise Http404
	return itinerary

@login_required
def invitation(request):
	context = {}
	if 'errors' in request.session:
		context["errors"] = request.session["errors"]
		del request.session["errors"]
	itinerary_id = get_itinerary_id_by_session(request)
	users = User.objects.all()
	context['itinerary_id'] = itinerary_id
	context['users'] = users
	return render(request, 'travelpad/invitation.html', context)
	
@login_required
@transaction.atomic
def invite(request):
	if request.method == "GET":
		print "invite POST only"
		return redirect("invitation")
	if not "username" in request.POST:
		print "invite without username"
		return redirect("invitation")
	try:
		user = User.objects.get(username=request.POST["username"])
	except:
		print "invite username not found"
		request.session['errors'] = "Username not existed"
		return redirect("invitation")
	itinerary = get_itinerary_by_session(request)
	itinerary.participants.add(user)
	return redirect("invitation")

