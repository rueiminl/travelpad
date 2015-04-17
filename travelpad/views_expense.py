from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseBadRequest
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
import dateutil.parser
from json import dumps
from travelpad.forms_expense import *
import json

    

@login_required    
def expense(request):
    if 'itinerary_id' not in request.session:
        return redirect(reverse(''))
    return render(request, 'travelpad/expense.html', {})
    
@login_required    
@transaction.atomic
def costs(request):
    itinerary_id = request.session['itinerary_id']
    itinerary = Itinerary.objects.get(id=itinerary_id)  
    if request.method == 'GET':
        costs = Cost.objects.filter(related_itinerary=itinerary)
        results = [cost.as_dict() for cost in costs]
        response_text = json.dumps(results)
        return HttpResponse(response_text, content_type='application/json')
    elif request.method == 'POST':
        print "post"

@login_required
@transaction.atomic
def costs_id(request, cost_id):
    itinerary_id = request.session['itinerary_id']
    itinerary = Itinerary.objects.get(id=itinerary_id)  
    try:
        cost = Cost.objects.get(id=cost_id)
        if request.method == 'PUT':
            in_data = json.loads(request.body)
            print in_data
            print cost
            participants = in_data.get('participant')
            partlist = []
            for participants in participants:
                partlist.append(participants.get('id'))
            print qq
            if in_data.get('owner'):
                owner = in_data.get('owner').get('id')
            else:
                owner = None
            form = CostForm(data=
                {'amount': in_data.get('amount'),
                'status': in_data.get('status'),
                'owner': owner,
                'note': in_data.get('note'),
                'participant': partlist}, instance=cost)
            print form
            if form.is_valid():
                pass
                new_cost = form.save()  
                results = new_cost.as_dict()
                response_text = json.dumps(results)          
                return HttpResponse(response_text, content_type='application/json')
            else:
                print form
                errors = []
                errors.append('Woops! Something wrong.')
                return HttpResponseBadRequest(json.dumps({'errors':errors}), content_type='application/json')
        elif request.method == 'DELETE':
            cost.delete()
            return HttpResponse({}, content_type='application/json')
    except ObjectDoesNotExist:
        errors = []
        errors.append('Cost not found.')
        return HttpResponseNotFound(json.dumps({'errors':errors}), content_type='application/json')
    except Exception as inst:
        print inst        