from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
import dateutil.parser
from json import dumps
import json

def demo(request):
	context = {}
    
	return render(request, 'travelpad/demo.html', context)

def calendar(request):
	context = {}
    
	return render(request, 'travelpad/calendar.html', context)
    
    
def get_calendar_events_json(request, itinerary_id):
    try:
        #request example: /myfeed.php?start=2013-12-01&end=2014-01-12&_=1386054751381
        start = dateutil.parser.parse(request.GET.get('start')) #ISO8601   
        end = dateutil.parser.parse(request.GET.get('end')) #ISO8601
        
        #TODO: filter(itinerary_id = itinerary_id)
        events = Event.objects.all().exclude(start_datetime__gt=end.isoformat()).exclude(end_datetime__lt=start.isoformat())
        
        print 'start: ' + start.isoformat() + ', end: ' + end.isoformat() + ', get ' + str(len(events)) + ' events'
        calendar_events = [] 
        for event in events:
            calendar_events.append(
                {'id' : event.id,
                'title':event.title, 
                'start': event.start_datetime.isoformat(), #ISO8601
                'end': event.end_datetime.isoformat(), #ISO8601
                #TODO: assign colors by event types
                'color' : 'blue'})
                
        #response_text = serializers.serialize('json', list)
        response_text = json.dumps(calendar_events)
        return HttpResponse(response_text, content_type='application/json')
    except Exception as inst:
        print inst

