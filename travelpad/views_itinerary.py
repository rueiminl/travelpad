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
from datetime import timedelta
from json import dumps
import json

@login_required
def demo(request):
    context = {}
    places = Event.objects.all()
    context['itinerary'] = {'id':1, 'start_date':'2015-03-23'}
    context['places'] = places
    return render(request, 'travelpad/demo.html', context)
    
@login_required
def itinerary(request, itinerary_id):
    request.session['itinerary_id'] = itinerary_id
    return redirect(reverse('schedule'))

@login_required
@transaction.atomic
def itinerary_json(request):
    try:
        itinerary_id = request.session['itinerary_id']
        itinerary = Itinerary.objects.get(id=itinerary_id)  
        if request.method == 'GET':
            response_text = json.dumps(itinerary.as_dict())
            return HttpResponse(response_text, content_type='application/json')
    except Exception as inst:
        print inst


@login_required
def schedule(request):
    if 'itinerary_id' not in request.session:
        return redirect(reverse('default'))
    try:
        itinerary_id = request.session['itinerary_id']
        itinerary = Itinerary.objects.get(id=itinerary_id)
        events = Event.objects.all()
        request.session['itinerary_id'] = itinerary_id
        return render(request, 'travelpad/schedule.html', {'itinerary' : itinerary, 'events' : events})
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Todo not found</h1>')
    except Exception as inst:
        print inst    

    
@login_required    
def get_calendar_events_json(request, itinerary_id):
    if 'itinerary_id' not in request.session:
        return HttpResponseNotFound('<h1>Event not found</h1>')
    itinerary_id = request.session['itinerary_id']
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
  
    #request example: /myfeed.php?start=2013-12-01&end=2014-01-12&_=1386054751381
    start = dateutil.parser.parse(request.GET.get('start')) #ISO8601   
    end = dateutil.parser.parse(request.GET.get('end')) #ISO8601
    
    events = Event.objects.filter(related_itinerary=itinerary).exclude(start_datetime__gt=end.isoformat()).exclude(end_datetime__lt=start.isoformat()).order_by('start_datetime') # order by start_datetime so that map view can construct routes
    trans = Transportation.objects.filter(related_itinerary=itinerary).exclude(start_datetime__gt=end.isoformat()).exclude(end_datetime__lt=start.isoformat())
    print 'start: ' + start.isoformat() + ', end: ' + end.isoformat() + ', get ' + str(len(events)) + ' events'
    print 'start: ' + start.isoformat() + ', end: ' + end.isoformat() + ', get ' + str(len(trans)) + ' trans'
    calendar_events = [] 

    # calendar background
    for n in range(int ((itinerary.end_date - itinerary.start_date).days) + 1): # +1 to include end_date
        d = itinerary.start_date + timedelta(n)
        calendar_events.append({
            'start': datetime.combine(d, datetime.min.time()).isoformat(),#date.replace(hour=00, minute=00).isoformat(),
            'end': datetime.combine(d, datetime.max.time()).isoformat(),#date.replace(hour=23, minute=59).isoformat(),
            'rendering': 'background',
            'className': 'background',
        })
    for event in events:
        try:
            event_json = event.as_dict()      
            event_json.update({
            # 'start': timezone.localtime(event.start_datetime).isoformat(),#event.start_datetime.isoformat(), #ISO8601
            # 'end': timezone.localtime(event.end_datetime).isoformat(),#event.end_datetime.isoformat(), #ISO8601
                'className' : [event.type, 'proposed' if event.proposed else ''], # attraction, hotel, restaurant
            })
        except Exception as inst:
            print inst
        calendar_events.append(event_json)
    for tran in trans:
        tran_json = tran.as_dict()
        tran_json.update({
            # 'start': timezone.localtime(tran.start_datetime).isoformat(),#event.start_datetime.isoformat(), #ISO8601
            # 'end': timezone.localtime(tran.end_datetime).isoformat(),#event.end_datetime.isoformat(), #ISO8601
            'editable' : False, # disable time ediable for transportation
            'className' : 'transportation'})
        calendar_events.append(tran_json)           
    response_text = json.dumps(calendar_events)
    return HttpResponse(response_text, content_type='application/json')


@login_required    
def todo(request):
    if 'itinerary_id' not in request.session:
        return redirect(reverse('default'))
    return render(request, 'travelpad/todo.html', {})

@login_required
@transaction.atomic
def todo_json(request):
    itinerary_id = request.session['itinerary_id']
    itinerary = Itinerary.objects.get(id=itinerary_id)  
    if request.method == 'GET':
        todos = Todo.objects.filter(related_itinerary=itinerary)
        results = [todo.as_dict() for todo in todos]
        response_text = json.dumps(results)
        return HttpResponse(response_text, content_type='application/json')
    elif request.method == 'POST':
        entry = Todo(created_by=request.user, related_itinerary=itinerary)
        in_data = json.loads(request.body)
        form = TodoForm(data=
            {'task': in_data.get('task'),
            'status': in_data.get('status'),
            'owner': in_data.get('owner').get('id') if hasattr(in_data.get('owner'), 'get') else None,
            'note': in_data.get('note')}, instance=entry)
        if form.is_valid():
            new_todo = form.save()  
            results = new_todo.as_dict()
            response_text = json.dumps(results)          
            return HttpResponse(response_text, content_type='application/json')
        else:
            errors = []
            errors.append('Woops! Something wrong.')
            return HttpResponseBadRequest(json.dumps({'errors':errors}), content_type='application/json')
 
@login_required
@transaction.atomic
def todo_id_json(request, todo_id):
    itinerary_id = request.session['itinerary_id']
    itinerary = Itinerary.objects.get(id=itinerary_id)  
    try:
        todo = Todo.objects.get(id=todo_id)
        if request.method == 'PUT':
            in_data = json.loads(request.body)
            print in_data
            form = TodoForm(data=
                {'task': in_data.get('task'),'id':todo.id,
                'status': in_data.get('status'),
                'owner': in_data.get('owner').get('id') if hasattr(in_data.get('owner'), 'get') else None,
                'note': in_data.get('note')}, instance=todo)
            if form.is_valid():
                new_todo = form.save()  
                results = new_todo.as_dict()
                response_text = json.dumps(results)          
                return HttpResponse(response_text, content_type='application/json')
            else:
                print form
                errors = []
                errors.append('Woops! Something wrong.')
                return HttpResponseBadRequest(json.dumps({'errors':errors}), content_type='application/json')
        elif request.method == 'DELETE':
            todo.delete()
            return HttpResponse({}, content_type='application/json')
    except ObjectDoesNotExist:
        errors = []
        errors.append('Todo not found.')
        return HttpResponseNotFound(json.dumps({'errors':errors}), content_type='application/json')
    except Exception as inst:
        print inst



@login_required    
def feed(request):
    if 'itinerary_id' not in request.session:
        return redirect(reverse('default'))
    return render(request, 'travelpad/feed.html', {})

@login_required
@transaction.atomic
def message_json(request):
    itinerary_id = request.session['itinerary_id']
    itinerary = Itinerary.objects.get(id=itinerary_id)  
    if request.method == 'GET':
        messages = Message.objects.filter(related_itinerary=itinerary)
        results = [message.as_dict() for message in messages]
        for message in results:
            message.update({'can_edit':True})
        response_text = json.dumps(results)
        return HttpResponse(response_text, content_type='application/json')
    elif request.method == 'POST':
        entry = Message(created_by=request.user, related_itinerary=itinerary)
        in_data = json.loads(request.body)
        form = MessageForm(data={'content': in_data.get('content')}, instance=entry)
        if form.is_valid():
            new_entry = form.save()  
            results = new_entry.as_dict()
            response_text = json.dumps(results)          
            return HttpResponse(response_text, content_type='application/json')
        else:
            errors = []
            errors.append('Woops! Something wrong.')
            return HttpResponseBadRequest(json.dumps({'errors':errors}), content_type='application/json')

@login_required
@transaction.atomic
def reply_json(request):
    if request.method == 'POST':
        in_data = json.loads(request.body)
        message_id = in_data.get('related_message')
        message = get_object_or_404(Message, id=message_id)
        entry = Reply(created_by=request.user, related_message=message)
        form = ReplyForm(data={'content': in_data.get('content')}, instance=entry)
        if form.is_valid():
            new_entry = form.save()  
            results = new_entry.as_dict()
            response_text = json.dumps(results)          
            return HttpResponse(response_text, content_type='application/json')
        else:
            errors = []
            errors.append('Woops! Something wrong.')
            return HttpResponseBadRequest(json.dumps({'errors':errors}), content_type='application/json')

@login_required
@transaction.atomic
def add_reply(request):
    errors = []   
    context = {}
    try:
        message_id = request.POST.get('message_id')
        last_update_reply = dateutil.parser.parse(request.POST.get('last_update_reply'))
        message = Message.objects.get(id=message_id)
        entry = Reply(created_by=request.user, related_message=message)
        reply_form = ReplyForm(request.POST, instance=entry)
        if not reply_form.is_valid():
            errors.append('You must enter content to reply.')
            return HttpResponse(json.dumps({'errors':errors}), content_type='application/json')
        else:
            reply_form.save()
        # query new comments
        replies = Reply.objects.filter(
            related_message=message,
            creation_time__gt=last_update_reply
        ).order_by('creation_time')
        print 'get ' + str(len(replies)) + ' comments'
        replies_json = []
        for reply in replies:
            replies_json.append({
                'created_by_username':reply.created_by.username,
                'created_by_uid': reply.created_by.id,
                'content': reply.content,
                'creation_time': reply.creation_time.isoformat(),
                # 'photo_url' : reverse('photo', kwargs={'uid':comment.created_by.id})
            })
        context['replies'] = replies_json
        # update last update time
        if replies:
            context['last_update_reply'] = max(reply.creation_time for reply in replies).isoformat()
        else:
            context['last_update_reply'] = ''
        
        response_text = json.dumps(context)
        return HttpResponse(response_text, content_type='application/json')
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Post not found</h1>')
    except Exception as inst:
        print inst
    
    