from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse, Http404
from django.templatetags.static import static
from django.core import serializers

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

# for reverse url
from django.core.urlresolvers import reverse

from datetime import datetime, time
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import json

from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

from travelpad.models import *
from travelpad.forms_event import *
from travelpad.views_itinerary import demo

def home_page(request):
    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view.
    #context = {}
    #posts = Post.objects.filter(user=request.user)
    #context = {'posts' : posts, 'user' : request.user}
    #return render(request, 'socialnetwork/profile.html', context)
    context = {}
    context['attractionform'] = AttractionForm(prefix = "a_")
    context['hotelform'] = HotelForm(prefix = "h_")
    context['transportationform'] = TransportationForm(prefix = "t_")
    context['restaurantform'] = RestaurantForm(prefix = "r_")
    return render(request, 'travelpad/addevent.html', context)
    
def eventedit(request):
    print request.user
    if request.method == 'GET':
        context = {}
        context['attractionform'] = AttractionForm(prefix = "a_")
        context['hotelform'] = HotelForm(prefix = "h_")
        context['transportationform'] = TransportationForm(prefix = "t_")
        context['restaurantform'] = RestaurantForm(prefix = "r_")
        return render(request, 'travelpad/EventWindow.html', context)
    if request.POST['eventId']:
        return eventeditwithID(request)
    context = {}
    errors = []
    context['errors'] = errors
    success = 1
    if 'save' in request.POST:
        isproposed = False;
    elif 'propose' in request.POST:
        isproposed = True;
        
    #if request.POST['submit'] == 'save':
    #    isproposed = False;
    #elif request.POST['submit'] == 'propose':
    #    isproposed = True;
    
    if request.user:
        new_user = request.user
    else:
        try:
            new_user = User.objects.get(username="username")
        except ObjectDoesNotExist:
            new_user = User.objects.create_user(username="username", password="password1")
            new_user.save()
        
    if (not request.POST['tabName']) or (request.POST['tabName']=="Attraction"):
        newevent = Event(user = new_user, type="attraction",proposed = isproposed)
        form = AttractionForm(request.POST, prefix = "a_")
    elif request.POST['tabName']=="Hotel":
        newevent = Event(user = new_user, type="hotel",proposed = isproposed)
        form = HotelForm(request.POST, prefix = "h_")
    elif request.POST['tabName']=="Transportation":
        newevent = Event(user = new_user, type="transportation",proposed = isproposed)
        form = TransportationForm(request.POST, prefix = "t_")
    elif request.POST['tabName']=="Restaurant":
        newevent = Event(user = new_user, type="restaurant",proposed = isproposed)
        form = RestaurantForm(request.POST, prefix = "r_")
    if form.is_valid():
        newevent.title = form.cleaned_data['title']
        thistinery = Itinerary.objects.get(id = request.session["itinerary_id"])
        newevent.related_itinerary = thistinery 
        #newevent.start_date = form.cleaned_data['start_date']
        #newevent.start_time = form.cleaned_data['start_time']
        #newevent.end_date = form.cleaned_data['end_date']
        #newevent.end_time = form.cleaned_data['end_time']
        stime = datetime.combine(form.cleaned_data['start_date'], form.cleaned_data['start_time'])
        etime = datetime.combine(form.cleaned_data['end_date'], form.cleaned_data['end_time'])
        newevent.start_datetime  = timezone.make_aware(stime, timezone.get_current_timezone())
        newevent.end_datetime = timezone.make_aware(etime, timezone.get_current_timezone())
        newevent.note = form.cleaned_data['note']
        newevent.place_id = request.POST['placeId']
        newevent.place_name = request.POST['placeName']
        s = request.POST['coordinate'][1:-1]
        tmp = s.split(', ')
        if (len(tmp) < 2):
            success = 0
            errors.append("You have to input the place you are going:");
        overlap = Event.objects.filter(related_itinerary__id=request.session["itinerary_id"]).filter(start_datetime__lt=newevent.end_datetime).filter(end_datetime__gt=newevent.start_datetime)
        if overlap.count() > 0: #overlap
            success = 0
            errors.append("The time overlaps with another event:");
        if success == 1:
            newevent.place_latitude = tmp[0]
            newevent.place_longitude = tmp[1]
            newevent.save()
            thistinery = Itinerary.objects.get(id = request.session["itinerary_id"])
            if (form.cleaned_data['todo']):
                newtodo = Todo(task = form.cleaned_data['todo'], status = "pending", created_by = new_user, related_event = newevent, related_itinerary = thistinery)
                newtodo.save()
            if (form.cleaned_data['cost']):
                newcost = Cost(amount = form.cleaned_data['cost'], isall = form.cleaned_data['split'], status = "New", created_by = new_user, related_event = newevent, related_itinerary = thistinery)
                newcost.save()
            strange = datetime.combine(form.cleaned_data['start_date'], time(0, 0, 0))
            srange = timezone.make_aware(strange, timezone.get_current_timezone())
            erange = srange + timezone.timedelta(days=1)
            try:
                pevent = Event.objects.filter(related_itinerary__id=request.session["itinerary_id"]).filter(end_datetime__range=[srange,newevent.start_datetime]).latest("end_datetime")
                try:
                    ptrans = pevent.pre
                    tempplace = ptrans.destination
                    temptime = ptrans.end_datetime
                    ptrans.end_datetime = newevent.start_datetime
                    ptrans.destination = newevent
                    ptrans.save()
                    newtrans = Transportation(user = new_user, type = "car", start_datetime = newevent.end_datetime, end_datetime = temptime, source = newevent, destination = tempplace, related_itinerary = thistinery)
                    newtrans.save()
                except ObjectDoesNotExist:
                    newtrans = Transportation(user = new_user, type = "car", start_datetime = pevent.end_datetime, end_datetime = newevent.start_datetime, source = pevent, destination = newevent, related_itinerary = thistinery)
                    newtrans.save()
            # first event of the day
            except ObjectDoesNotExist:
                try:
                    nevent = Event.objects.filter(related_itinerary__id=request.session["itinerary_id"]).filter(start_datetime__range=[newevent.end_datetime,erange]).earliest("start_datetime")
                    newtrans = Transportation(user = new_user, type = "car", start_datetime = newevent.end_datetime, end_datetime = nevent.start_datetime, source = newevent, destination = nevent, related_itinerary = thistinery)
                    newtrans.save()
                except ObjectDoesNotExist:
                    print "first event"
                    pass
            context['success'] = 1
    else:
        errors.append("Please check the message below:");
        success = 0
    #return render(request, 'travelpad/addevent.html', context)
    if success == 1:
        #return redirect(reverse('demo'))
        request.session["addevent"] = 1;
        return redirect(reverse('schedule'))
    else:
        context['attractionform'] = AttractionForm(request.POST, prefix = "a_")
        context['hotelform'] = HotelForm(request.POST, prefix = "h_")
        context['transportationform'] = TransportationForm(request.POST, prefix = "t_")
        context['restaurantform'] = RestaurantForm(request.POST, prefix = "r_")
        context['tabName'] = newevent.type
        context['iid'] = request.session["itinerary_id"]
        return render(request, 'travelpad/addevent_error.html', context)
        
def eventeditwithID(request):
    print request.user
    if request.method == 'GET':
        context = {}
        context['attractionform'] = AttractionForm(prefix = "a_")
        context['hotelform'] = HotelForm(prefix = "h_")
        context['transportationform'] = TransportationForm(prefix = "t_")
        context['restaurantform'] = RestaurantForm(prefix = "r_")
        return render(request, 'travelpad/EventWindow.html', context)

    context = {}
    errors = []
    context['errors'] = errors
    success = 1
    if 'save' in request.POST:
        isproposed = False;
    elif 'propose' in request.POST:
        isproposed = True;

    newevent = Event.objects.get(id = request.POST['eventId'])
    newevent.isproposed = isproposed
    if (not request.POST['tabName']) or (request.POST['tabName']=="Attraction"):
        form = AttractionForm(request.POST, prefix = "a_")
    elif request.POST['tabName']=="Hotel":
        form = HotelForm(request.POST, prefix = "h_")
    elif request.POST['tabName']=="Transportation":
        #form = TransportationForm(request.POST, prefix = "t_")
        return transporteditwithid(request)
    elif request.POST['tabName']=="Restaurant":
        form = RestaurantForm(request.POST, prefix = "r_")
    if form.is_valid():
        stime = datetime.combine(form.cleaned_data['start_date'], form.cleaned_data['start_time'])
        etime = datetime.combine(form.cleaned_data['end_date'], form.cleaned_data['end_time'])
        newevent.start_datetime  = timezone.make_aware(stime, timezone.get_current_timezone())
        newevent.end_datetime = timezone.make_aware(etime, timezone.get_current_timezone())
        newevent.note = form.cleaned_data['note']
        overlap = Event.objects.filter(related_itinerary__id=request.session["itinerary_id"]).filter(start_datetime__lt=newevent.end_datetime).filter(end_datetime__gt=newevent.start_datetime).exclude(id = request.POST['eventId'])
        if overlap.count() > 0: #overlap
            success = 0
            errors.append("The time overlaps with another event:")
        if success == 1:
            newevent.save()
            thistinery = Itinerary.objects.get(id = request.session["itinerary_id"])
            if (form.cleaned_data['todo']):
                newtodo = Todo(task = form.cleaned_data['todo'], status = "pending", created_by = new_user, related_event = newevent, related_itinerary = thistinery)
                newtodo.save()
            if (form.cleaned_data['cost']):
                newcost = Cost(amount = form.cleaned_data['cost'], isall = form.cleaned_data['split'], status = "New", created_by = new_user, related_event = newevent, related_itinerary = thistinery)
                newcost.save()
            # begin edit transportation
            strange = datetime.combine(form.cleaned_data['start_date'], time(0, 0, 0))
            srange = timezone.make_aware(strange, timezone.get_current_timezone())
            erange = srange + timezone.timedelta(days=1)
            needrelocate = False;
            hasprevious = False;
            
            try:
                ptrans = newevent.next
                hasprevious = True;
                try:
                    pevent = Event.objects.filter(related_itinerary__id=request.session["itinerary_id"]).filter(end_datetime__range=[srange,newevent.start_datetime]).latest("end_datetime")
                    if ptrans.source == pevent:
                        pass    #previous event unchanged, implies next event unchanged
                    else:
                        needrelocate = True    #previous event changed
                except ObjectDoesNotExist:
                    needrelocate = True    #has previous event, now hasnot
            except ObjectDoesNotExist:
                try:
                    ntrans = newevent.pre
                    try:
                        nevent = Event.objects.filter(related_itinerary__id=request.session["itinerary_id"]).filter(start_datetime__range=[newevent.end_datetime,erange]).earliest("start_datetime")
                        if ntrans.destination == nevent:
                            pass    #next event unchanged
                        else:
                            needrelocate = True    #next event changed
                    except ObjectDoesNotExist:
                        needrelocate = True    #has next event, now has not
                except ObjectDoesNotExist:
                    try:
                        pevent = Event.objects.filter(related_itinerary__id=request.session["itinerary_id"]).filter(end_datetime__range=[srange,newevent.start_datetime]).latest("end_datetime")
                        needrelocate = True    #don't have previous event, now has
                    except ObjectDoesNotExist:
                        try: 
                            nevent = Event.objects.filter(related_itinerary__id=request.session["itinerary_id"]).filter(start_datetime__range=[newevent.end_datetime,erange]).earliest("start_datetime")
                            needrelocate = True    #don't have next event, now has
                        except ObjectDoesNotExist:
                            pass #only event of the day
            
            if needrelocate == True:
                # remove transporation
                try:
                    ntrans = newevent.pre
                    if hasprevious == True:
                        ptrans = newevent.next
                        ptrans.end_datetime = ntrans.end_datetime
                        ptrans.destination = ntrans.destination
                        ntrans.delete()
                        ptrans.save()
                    else:
                        ntrans.delete()
                except ObjectDoesNotExist:
                    if hasprevious == True:
                        ptrans.delete()
                # now add new transporation
                try:
                    pevent = Event.objects.filter(related_itinerary__id=request.session["itinerary_id"]).filter(end_datetime__range=[srange,newevent.start_datetime]).latest("end_datetime")
                    try:
                        ptrans = pevent.pre
                        tempplace = ptrans.destination
                        temptime = ptrans.end_datetime
                        ptrans.end_datetime = newevent.start_datetime
                        ptrans.destination = newevent
                        ptrans.save()
                        newtrans = Transportation(user = request.user, type = "car", start_datetime = newevent.end_datetime, end_datetime = temptime, source = newevent, destination = tempplace, related_itinerary = thistinery)
                        newtrans.save()
                    except ObjectDoesNotExist:
                        newtrans = Transportation(user = request.user, type = "car", start_datetime = pevent.end_datetime, end_datetime = newevent.start_datetime, source = pevent, destination = newevent, related_itinerary = thistinery)
                        newtrans.save()
                # first event of the day
                except ObjectDoesNotExist:
                    try:
                        nevent = Event.objects.filter(related_itinerary__id=request.session["itinerary_id"]).filter(start_datetime__range=[newevent.end_datetime,erange]).earliest("start_datetime", related_itinerary = thistinery)
                        newtrans = Transportation(user = request.user, type = "car", start_datetime = newevent.end_datetime, end_datetime = nevent.start_datetime, source = newevent, destination = nevent)
                        newtrans.save()
                    except ObjectDoesNotExist:
                        print "first event"
                        pass
            else:
                try:
                    ptrans = newevent.next
                    ptrans.end_datetime = newevent.start_datetime
                    ptrans.save()
                except ObjectDoesNotExist:
                    pass
                try:
                    ntrans = newevent.pre
                    ntrans.start_datetime = newevent.end_datetime
                    ntrans.save()
                except ObjectDoesNotExist:
                    pass
            context['success'] = 1
    else:
        errors.append("Please check the message below:")
        success = 0
    #return render(request, 'travelpad/addevent.html', context)
    #return demo(request)
    if success == 1:
        #return redirect(reverse('demo'))
        return redirect(reverse('schedule'))
        
    else:
        context['attractionform'] = AttractionForm(request.POST, prefix = "a_")
        context['hotelform'] = HotelForm(request.POST, prefix = "h_")
        context['transportationform'] = TransportationForm(request.POST, prefix = "t_")
        context['restaurantform'] = RestaurantForm(request.POST, prefix = "r_")
        context['tabName'] = newevent.type
        context['id'] = newevent.id
        context['place'] = newevent.place_name
        context['iid'] = request.session["itinerary_id"]
        return render(request, 'travelpad/addevent_error.html', context)
        
def editeventtime(request):
    if request.method == 'GET':
        raise Http404  

    context = {}
    errors = []
    context['errors'] = errors
    success = 1
    newevent = Event.objects.get(id = request.POST['eid'])
    strange = datetime.combine(newevent.start_datetime.date(), datetime.strptime(request.POST['stime'], '%H:%M').time())
    srange = timezone.make_aware(strange, timezone.get_current_timezone())
    etrange = datetime.combine(newevent.end_datetime.date(), datetime.strptime(request.POST['etime'], '%H:%M').time())
    erange = timezone.make_aware(etrange, timezone.get_current_timezone())
    newevent.start_datetime = srange
    newevent.end_datetime = erange
    newevent.save()
    try:
        ptrans = newevent.next
        ptrans.end_datetime = srange
        ptrans.save()
    except ObjectDoesNotExist:
        pass
    try:
        ntrans = newevent.pre
        ntrans.start_datetime = erange
        ntrans.save()
    except ObjectDoesNotExist:
        pass
    return HttpResponse("success")
        
def transporteditwithid(request):
    trans = Transportation.objects.get(id = request.POST['eventId'])
    form = TransportationForm(request.POST, prefix = "t_")
    #print request.session["itinerary_id"] 
    if form.is_valid():
        trans.type = form.cleaned_data['format']
        trans.save()
    #return redirect(reverse('demo'))
    return redirect(reverse('schedule'))
        
def getevent(request):
    print request.POST['eid']
    event = Event.objects.get(id = request.POST['eid'])
    dictionary = event.as_dict()
    return HttpResponse(json.dumps({"data": dictionary}), content_type='application/json')
    
def gettransport(request):
    print request.POST['eid']
    trans = Transportation.objects.get(id = request.POST['eid'])
    dictionary = trans.as_dict()
    return HttpResponse(json.dumps({"data": dictionary}), content_type='application/json')
    
def deleteevent(request):
    print request.POST['eid']
    event = Event.objects.get(id = request.POST['eid'])
    try:
        ptrans = event.next
        ntrans = event.pre
        ptrans.end_datetime = ntrans.end_datetime
        ptrans.destination = ntrans.destination
        ntrans.delete()
        ptrans.save()
    except ObjectDoesNotExist:
        #don't care because django will delete foreign key for us
        pass
    event.delete()
    return HttpResponse("success")