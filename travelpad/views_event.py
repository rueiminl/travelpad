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

from datetime import datetime
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
    context = {}
    errors = []
    context['errors'] = errors
    success = 1
    if 'save' in request.POST:
        isproposed = False;
    elif 'propose' in request.POST:
        isproposed = True;
    try:
        new_user = User.objects.get(username="username")
    except ObjectDoesNotExist:
        new_user = User.objects.create_user(username="username", password="password1")
        new_user.save()
        
    #newevent = Event(user=request.user, type="attraction",proposed = isproposed)
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
        overlap = Event.objects.filter(start_datetime__lt=newevent.end_datetime).filter(end_datetime__gt=newevent.start_datetime)
        if overlap.count() > 0: #overlap
            success = 0
            errors.append("The time overlaps with another event:");
        if success == 1:
            newevent.place_latitude = tmp[0]
            newevent.place_longitude = tmp[1]
            newevent.save()
            if (form.cleaned_data['todo']):
                newtodo = Todo(task = form.cleaned_data['todo'], status = "New", created_by = "username", related_event = form.cleaned_data['title'])
                newtodo.save()
            context['success'] = 1
    else:
        errors.append("Please check the message below:");
        success = 0
    #return render(request, 'travelpad/addevent.html', context)
    #return demo(request)
    if success == 1:
        return redirect(reverse('demo'))
    else:
        context['attractionform'] = AttractionForm(request.POST, prefix = "a_")
        context['hotelform'] = HotelForm(request.POST, prefix = "h_")
        context['transportationform'] = TransportationForm(request.POST, prefix = "t_")
        context['restaurantform'] = RestaurantForm(request.POST, prefix = "r_")
        context['tabName'] = newevent.type
        return render(request, 'travelpad/addevent_error.html', context)
 
