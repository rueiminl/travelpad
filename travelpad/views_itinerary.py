from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
import dateutil.parser
from json import dumps
import json

demo_itinerary = {'id':1, 'start_date':'2015-03-23'}

@login_required
def demo(request):
    context = {}
    places = Event.objects.all()
    context['itinerary'] = {'id':1, 'start_date':'2015-03-23'}
    context['places'] = places
    return render(request, 'travelpad/demo.html', context)

@login_required    
def todo(request):
    context = {}
    todoes = Todo.objects.all()
    context['todoes'] = todoes
    context['todo_form'] = TodoForm()
    print 'get ' + str(len(todoes)) + ' todoes'
    return render(request, 'travelpad/todo.html', context)

@login_required
@transaction.atomic
def add_todo(request):
    errors = []   
    try:
        entry = Todo(created_by=request.user)
        todo_form = TodoForm(request.POST, instance=entry)
        if not todo_form.is_valid():
            errors.append('You must enter content to post.')
            return HttpResponse(json.dumps({'errors':errors}), content_type='application/json')
        else:
            todo_form.save()
            return get_post_json(request)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Todo not found</h1>')
    except Exception as inst:
        print inst


@login_required
def calendar(request):
	context = {}
    
	return render(request, 'travelpad/calendar.html', context)
    
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
def feed(request, itinerary_id):
    context = {}
    try:
        itinerary = Itinerary.objects.get(id=itinerary_id)
        messages = Message.objects.filter(related_itinerary=itinerary).order_by('-creation_time')
        # context['itinerary'] = {'id':1, 'start_date':'2015-03-23'}
#         messages = Message.objects.all().order_by('-creation_time')
        context['itinerary'] = itinerary
        context['messages'] = messages
        last_update = ''
        for message in messages:
            message.replies = Reply.objects.filter(related_message=message).order_by('creation_time')
            # last_update = max(last_update, message.timestamp)
        # if messages:
 #            # last_update = messages[0].creation_time.isoformat()
 #            #update_times = max(messages, key=lambda x:x['timestamp'])#[x['timestamp'] for x in messages]
 #            update_times = max(d['price'] for m in messages)
 #            print update_time
 #            last_update = max(update_times)
 #        else:
 #            last_update = ''
        context['last_update'] = ''
        context['last_update'] = max(message.timestamp for message in messages)
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
        messages = Message.objects.filter(timestamp__gt=last_update, related_itinerary=itinerary).order_by('-creation_time')
        print 'get ' + str(len(messages)) + ' messages'
        context['last_update'] = ''
        context['last_update'] = max(message.timestamp for message in messages).isoformat()
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
            messages_json.append(
                {'id' : message.id,
                'created_by_username':message.created_by.username, 
                'created_by_uid': message.created_by.id, 
                'content': message.content,
                'creation_time': message.creation_time.isoformat(),
                # 'last_update_comment' : post.last_update_comment,
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
    # try:
#         post_id = request.POST.get('post_id')
#         last_update = request.POST.get('last_update_comment')
#         # add comment
#         post = Post.objects.get(id=post_id)
#         entry = Comment(created_by=request.user, related_post=post)
#         comment_form = CommentForm(request.POST, instance=entry)
#         if not comment_form.is_valid():
#             errors.append('You must enter content to comment.')
#             return HttpResponse(json.dumps({'errors':errors}), content_type='application/json')
#         else:
#             comment_form.save()
#         # query new comments
#         comments = Comment.objects.all().filter(
#             related_post=post,
#             creation_time__gt=timestamp_to_datetime(last_update)
#         ).order_by('creation_time')
#         print 'get ' + str(len(comments)) + ' comments'
#         comments_json = []
#         for comment in comments:
#             comments_json.append({
#                 'created_by_username':comment.created_by.username,
#                 'created_by_uid': comment.created_by.id,
#                 'content': comment.content,
#                 'creation_time': datetime_to_timestamp(comment.creation_time),
#                 'photo_url' : reverse('photo', kwargs={'uid':comment.created_by.id})
#             })
#         # update last update time
#         new_update = last_update
#         max_creation_time = Comment.objects.filter(
#             related_post=post,
#             creation_time__gt=timestamp_to_datetime(last_update)
#         ).order_by('creation_time').aggregate(Max('creation_time'))
#         if max_creation_time['creation_time__max']:
#             new_update = datetime_to_timestamp(max_creation_time['creation_time__max'])
#         # generate json
#         data = {
#             'last_update_comment' : new_update,
#             'comments': comments_json,
#         }
#         response_text = json.dumps(data)
#         return HttpResponse(response_text, content_type='application/json')
#     except ObjectDoesNotExist:
#         return HttpResponseNotFound('<h1>Post not found</h1>')
#     except Exception as inst:
#         print inst
    
    