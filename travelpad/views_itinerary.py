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
        return redirect(reverse(''))
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
        return redirect(reverse(''))
    return render(request, 'travelpad/todo.html', {})
# def todo(request):
#     if 'itinerary_id' not in request.session:
#         return redirect(reverse(''))
#     try:
#         itinerary_id = request.session['itinerary_id']
#         itinerary = Itinerary.objects.get(id=itinerary_id)
#         context = {}
#         todoes = Todo.objects.filter(related_itinerary=itinerary)
#         if todoes:
#             request.session['todo_last_update'] = max(todo.creation_time for todo in todoes).isoformat()
#         context['todoes'] = todoes
#         context['participants'] = itinerary.participants.all()
#         # context['todo_form'] = TodoForm()
#         print 'get ' + str(len(todoes)) + ' todoes'
#         return render(request, 'travelpad/todo.html', context)
#     except ObjectDoesNotExist:
#         return HttpResponseNotFound('<h1>Todo not found</h1>')
#     except Exception as inst:
#         print inst

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
            'owner': in_data.get('owner').get('id'),
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
            print todo
            form = TodoForm(data=
                {'task': in_data.get('task'),'id':todo.id,
                'status': in_data.get('status'),
                'owner': in_data.get('owner').get('id'),
                'note': in_data.get('note')}, instance=todo)
            print form
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
        return redirect(reverse(''))
    return render(request, 'travelpad/feed.html', {})
    # try:
#         context = {}
#         itinerary_id = request.session['itinerary_id']
#         itinerary = Itinerary.objects.get(id=itinerary_id)
#         messages = Message.objects.filter(related_itinerary=itinerary).order_by('-creation_time')
#         # context['itinerary'] = {'id':1, 'start_date':'2015-03-23'}
# #         messages = Message.objects.all().order_by('-creation_time')
#         context['itinerary'] = itinerary
#         context['messages'] = messages
#         last_update = ''
#         for message in messages:
#             message.replies = Reply.objects.filter(related_message=message).order_by('creation_time')
#             if message.replies:
#                 message.last_update_reply = max(reply.creation_time for reply in message.replies).isoformat()
#             else :
#                 message.last_update_reply = ''
#         if messages:
#             context['last_update'] = max(message.creation_time for message in messages)
#         else:
#             context['last_update'] = ''
#
#     except ObjectDoesNotExist:
#         return HttpResponseNotFound('<h1>Itinerary not found</h1>')
#     return render(request, 'travelpad/feed.html', context)

@login_required
@transaction.atomic
def message_json(request):
    itinerary_id = request.session['itinerary_id']
    itinerary = Itinerary.objects.get(id=itinerary_id)  
    if request.method == 'GET':
        messages = Message.objects.filter(related_itinerary=itinerary)
        results = [message.as_dict() for message in messages]
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

# @login_required
# @transaction.atomic
# def add_message(request):
#     errors = []
#     try:
#         itinerary_id = request.POST.get('itinerary_id')
#         itinerary = Itinerary.objects.get(id=itinerary_id)
#         entry = Message(created_by=request.user, related_itinerary=itinerary)
#         message_form = MessageForm(request.POST, instance=entry)
#         if not message_form.is_valid():
#             errors.append('You must enter content to post.')
#             return HttpResponse(json.dumps({'errors':errors}), content_type='application/json')
#         else:
#             message_form.save()
#             return get_message_json(request, itinerary_id)
#     except ObjectDoesNotExist:
#         return HttpResponseNotFound('<h1>Recourse not found</h1>')
#     except Exception as inst:
#         print inst
#
# @login_required
# def get_message_json(request, itinerary_id):
#     context = {}
#     try:
#         itinerary = Itinerary.objects.get(id=itinerary_id)
#         last_update = dateutil.parser.parse(request.POST.get('last_update'))
#         # print last_update
#         messages = Message.objects.filter(creation_time__gt=last_update, related_itinerary=itinerary).order_by('-creation_time')
#         print 'get ' + str(len(messages)) + ' messages'
#         if messages:
#             context['last_update'] = max(message.creation_time for message in messages).isoformat()
#         else:
#             context['last_update'] = ''
#
#         messages_json = []
#         for message in messages:
#             message.replies = Reply.objects.filter(related_message=message).order_by('creation_time')
#             replies_json = []
#             for reply in message.replies:
#                 replies_json.append({
#                     'created_by_username':reply.created_by.username,
#                     'created_by_uid': reply.created_by.id,
#                     'content': reply.content,
#                     'creation_time': reply.creation_time.isoformat(),
#                     # 'photo_url' : reverse('photo', kwargs={'uid':comment.created_by.id})
#                 })
#             if message.replies:
#                 last_update_reply = max(reply.creation_time for reply in message.replies).isoformat()
#             else:
#                 last_update_reply = ''
#
#             messages_json.append(
#                 {'id' : message.id,
#                 'created_by_username':message.created_by.username,
#                 'created_by_uid': message.created_by.id,
#                 'content': message.content,
#                 'creation_time': message.creation_time.isoformat(),
#                 'last_update_reply' : last_update_reply,
#                 'replies' : replies_json})
#         context['messages'] = messages_json
#         response_text = json.dumps(context)
#         return HttpResponse(response_text, content_type='application/json')
#     except Exception as inst:
#         print inst


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
    
    