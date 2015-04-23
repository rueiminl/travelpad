from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
from travelpad.forms_itineraries import *
from travelpad.views_itinerary import demo
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import send_mail

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
def participant_json(request):
	context = {}
	if not 'itinerary_id' in request.session:
		results = {"success":"false", "errors":"Unknown itinerary"}
		return HttpResponse(json.dumps(results), content_type='application/json')
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
			email_body = """
Just a reminder that you've been invited to the itinerary \"%s\".
Please don't forget to come to say hi to other participants.

Cheers!
TravelPad team
""" % (itinerary.title)
			send_mail(subject="[TravelPad] invitation notification", message= email_body, from_email="rueiminl@andrew.cmu.edu", recipient_list=[user.email])
		else:
			if not Itinerary.objects.filter(id=itinerary_id).filter(participants=user).exists():
				print "Warn: username does not participate yet"
				results = {"success":"false","errors":"The user is not participated yet"}
				return HttpResponse(json.dumps(results), content_type='application/json')
			itinerary.participants.remove(user)
			email_body = """
Just a reminder that you've been kicked out by \"%s\" from the itinerary \"%s\".
If any question, please contact the kicker directly...

Cheers!
TravelPad team
""" % (request.user.username, itinerary.title)
			send_mail(subject="[TravelPad] invitation notification", message= email_body, from_email="rueiminl@andrew.cmu.edu", recipient_list=[user.email])
		results = {"success":"true",
		           "participant": {"id" : user.id, "username" : user.username}
		          }
		return HttpResponse(json.dumps(results), content_type='application/json')
	