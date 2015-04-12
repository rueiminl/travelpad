from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
import dateutil.parser
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
def todo_json(request):
    context = {}
    itinerary_id = request.session['itinerary_id']
    itinerary = Itinerary.objects.get(id=itinerary_id)
    
    if request.method == 'GET':
        todos = Todo.objects.filter(related_itinerary=itinerary)
        results = [todo.as_dict() for todo in todos]
        response_text = json.dumps(results)
        return HttpResponse(response_text, content_type='application/json')


@login_required
@transaction.atomic
def add_todo(request):
    errors = []   
    try:
        itinerary_id = request.session['itinerary_id']
        itinerary = Itinerary.objects.get(id=itinerary_id)
        entry = Todo(created_by=request.user, related_itinerary=itinerary)
        todo_form = TodoForm(request.POST, instance=entry)
        if not todo_form.is_valid():
            errors.append('You must enter content to post.')
            return HttpResponse(json.dumps({'errors':errors}), content_type='application/json')
        else:
            todo_form.save()
            return get_todo_json(request)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Todo not found</h1>')
    except Exception as inst:
        print inst

@login_required
@transaction.atomic
def update_todo(request, todo_id):
    errors = []   
    try:
        entry = Todo.objects.get(id=todo_id)
        todo_form = TodoForm(request.POST, instance=entry)
        if not todo_form.is_valid():
            print todo_form.errors
            errors.append('You must enter content to post.')
            return HttpResponse(json.dumps({'errors':errors}), content_type='application/json')
        else:
            todo_form.save()
        return get_todo_json(request)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Todo not found</h1>')
    except Exception as inst:
        print inst
        
@login_required
@transaction.atomic
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete();
    return get_todo_json(request)


@login_required
def get_todo_json(request):
    context = {}
    try:
        itinerary_id = request.session['itinerary_id']
        itinerary = Itinerary.objects.get(id=itinerary_id)
        if 'todo_last_update' in request.session:
            last_update = dateutil.parser.parse(request.session['todo_last_update'])
            todoes = Todo.objects.filter(related_itinerary=itinerary, creation_time__gt=last_update)
        else:
            todoes = Todo.objects.filter(related_itinerary=itinerary)
        print 'get ' + str(len(todoes)) + ' todoes'
        if todoes:
            request.session['todo_last_update'] = max(todo.creation_time for todo in todoes).isoformat()
        
        todoes_json = [] 
        for todo in todoes:
            todo_json = {'id' : todo.id,
                'created_by_username':todo.created_by.username, 
                'created_by_uid': todo.created_by.id, 
                'task': todo.task,
                'status': todo.status,
                # 'onwer_username':todo.owner.username,
#                 'onwer_uid': todo.owner.id,
                'note': todo.note,
                'creation_time': todo.creation_time.isoformat(),
            }
            if todo.owner:
                todo_json['onwer_username'] = todo.owner.username
                todo_json['onwer_uid'] = todo.owner.id
            todoes_json.append(todo_json)
        context['todoes'] = todoes_json
        response_text = json.dumps(context)
        return HttpResponse(response_text, content_type='application/json')
    except Exception as inst:
        print inst

# @login_required
# def calendar(request):
#     context = {}
#
#     return render(request, 'travelpad/calendar.html', context)
    
@login_required    
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


@login_required    
def feed(request):
    if 'itinerary_id' not in request.session:
        return redirect(reverse(''))
    try:
        context = {}
        itinerary_id = request.session['itinerary_id']
        itinerary = Itinerary.objects.get(id=itinerary_id)
        messages = Message.objects.filter(related_itinerary=itinerary).order_by('-creation_time')
        # context['itinerary'] = {'id':1, 'start_date':'2015-03-23'}
#         messages = Message.objects.all().order_by('-creation_time')
        context['itinerary'] = itinerary
        context['messages'] = messages
        last_update = ''
        for message in messages:
            message.replies = Reply.objects.filter(related_message=message).order_by('creation_time')     
            if message.replies:
                message.last_update_reply = max(reply.creation_time for reply in message.replies).isoformat()
            else :
                message.last_update_reply = ''
        # if messages:
 #            # last_update = messages[0].creation_time.isoformat()
 #            #update_times = max(messages, key=lambda x:x['timestamp'])#[x['timestamp'] for x in messages]
 #            update_times = max(d['price'] for m in messages)
 #            print update_time
 #            last_update = max(update_times)
 #        else:
 #            last_update = ''
        if messages:
            context['last_update'] = max(message.creation_time for message in messages)
        else:
            context['last_update'] = ''
        
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Itinerary not found</h1>')
    return render(request, 'travelpad/feed.html', context)

@login_required
@transaction.atomic
def add_message(request):
    errors = []   
    try:
        itinerary_id = request.POST.get('itinerary_id')
        itinerary = Itinerary.objects.get(id=itinerary_id)
        entry = Message(created_by=request.user, related_itinerary=itinerary)
        message_form = MessageForm(request.POST, instance=entry)
        if not message_form.is_valid():
            errors.append('You must enter content to post.')
            return HttpResponse(json.dumps({'errors':errors}), content_type='application/json')
        else:
            message_form.save()
            return get_message_json(request, itinerary_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Recourse not found</h1>')
    except Exception as inst:
        print inst
    
@login_required
def get_message_json(request, itinerary_id):
    context = {}
    try:
        itinerary = Itinerary.objects.get(id=itinerary_id)
        last_update = dateutil.parser.parse(request.POST.get('last_update'))
        # print last_update
        messages = Message.objects.filter(creation_time__gt=last_update, related_itinerary=itinerary).order_by('-creation_time')
        print 'get ' + str(len(messages)) + ' messages'
        if messages:
            context['last_update'] = max(message.creation_time for message in messages).isoformat()
        else:
            context['last_update'] = ''
        
        messages_json = [] 
        for message in messages:
            message.replies = Reply.objects.filter(related_message=message).order_by('creation_time')
            replies_json = []
            for reply in message.replies:
                replies_json.append({
                    'created_by_username':reply.created_by.username, 
                    'created_by_uid': reply.created_by.id, 
                    'content': reply.content,
                    'creation_time': reply.creation_time.isoformat(),
                    # 'photo_url' : reverse('photo', kwargs={'uid':comment.created_by.id})
                })
            if message.replies:
                last_update_reply = max(reply.creation_time for reply in message.replies).isoformat()
            else:
                last_update_reply = ''
            
            messages_json.append(
                {'id' : message.id,
                'created_by_username':message.created_by.username, 
                'created_by_uid': message.created_by.id, 
                'content': message.content,
                'creation_time': message.creation_time.isoformat(),
                'last_update_reply' : last_update_reply,
                'replies' : replies_json})
        context['messages'] = messages_json
        # for message in messages:
#             post.comments = Comment.objects.filter(related_post=post).order_by('creation_time')
#             max_creation_time = Comment.objects.filter(related_post=post).order_by('creation_time').aggregate(Max('creation_time'))
#             if max_creation_time['creation_time__max']:
#                 post.last_update_comment = datetime_to_timestamp(max_creation_time['creation_time__max'])
#             else:
#                 post.last_update_comment = '0'
#             comments_json = []
#             for comment in post.comments:
#                 comments_json.append({
#                     'created_by_username':comment.created_by.username,
#                     'created_by_uid': comment.created_by.id,
#                     'content': comment.content,
#                     'creation_time': datetime_to_timestamp(comment.creation_time),
#                     'photo_url' : reverse('photo', kwargs={'uid':comment.created_by.id})
#                 })#int(time.mktime(comment.creation_time.timetuple()))})
#             messages_json.append(
#                 {'id' : post.id,
#                 'created_by_username':post.created_by.username,
#                 'created_by_uid': post.created_by.id,
#                 'content': post.content,
#                 'creation_time': datetime_to_timestamp(post.creation_time),#int(time.mktime(post.creation_time.timetuple())),
#                 'last_update_comment' : post.last_update_comment,
#                 'comments' : comments_json})
#         new_update = last_update
#         if posts:
#             new_update = datetime_to_timestamp(posts[0].creation_time)
#         data = {
#             'last_update' : new_update,
#             'posts': posts_json,
#         }
        #response_text = serializers.serialize('json', list)
        response_text = json.dumps(context)
        return HttpResponse(response_text, content_type='application/json')
    except Exception as inst:
        print inst


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
    
    