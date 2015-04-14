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
import json

    

@login_required    
def expense(request):
    if 'itinerary_id' not in request.session:
        return redirect(reverse(''))
    return render(request, 'travelpad/expense.html', {})
    
@login_required    
def costs(request):
    itinerary_id = request.session['itinerary_id']
    itinerary = Itinerary.objects.get(id=itinerary_id)  
    if request.method == 'GET':
        costs = Cost.objects.filter(related_itinerary=itinerary)
        results = [cost.as_dict() for cost in costs]
        response_text = json.dumps(results)
        return HttpResponse(response_text, content_type='application/json')
        