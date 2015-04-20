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
	print request.POST
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

@login_required
def participant_json(request):
	context = {}
	itinerary_id = request.session['itinerary_id']
	itinerary = Itinerary.objects.get(id=itinerary_id)    
	if request.method == 'GET':
		results = []
		results = [participant.as_dict() for participant in itinerary.participants.all()]
		for result in results:
			del result["photo"]
		response_text = json.dumps(results)
		print response_text
		return HttpResponse(response_text, content_type='application/json')
	elif request.method == 'POST':
		if not 'username' in request.POST:
			print "no username field in request.POST"
			return redirect("invitation")
		if not 'type' in request.POST:
			print "no type field in request.POST"
			return redirect("invitation")
		try:
			user = User.objects.get(username = request.POST["username"])
		except:
			print "Warn: username not exist"
			results = {"success":"false","errors":"Username not exist"}
			return HttpResponse(json.dumps(results), content_type='application/json')
		if request.POST['type'] == 'add':
			if Itinerary.objects.filter(id=itinerary_id).filter(participants=user).exists():
				print "Warn: username has participated already"
				results = {"success":"false","errors":"The user has participated already"}
				return HttpResponse(json.dumps(results), content_type='application/json')
			itinerary.participants.add(user)
		else:
			if not Itinerary.objects.filter(id=itinerary_id).filter(participants=user).exists():
				print "Warn: username does not participate yet"
				results = {"success":"false","errors":"The user is not participated yet"}
				return HttpResponse(json.dumps(results), content_type='application/json')
			itinerary.participants.remove(user)
		results = {"success":"true",
		           "participant": {"id" : user.id, "username" : user.username}
		          }
		return HttpResponse(json.dumps(results), content_type='application/json')
	