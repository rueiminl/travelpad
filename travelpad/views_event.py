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
    return render(request, 'travelpad/addevent.html', context)

def eventedit(request):
    if request.method == 'GET':
        context = {}
        context['attractionform'] = AttractionForm()
        return render(request, 'travelpad/EventWindow.html', context)
    context = {}
    context['test'] = "active"
    if 'save' in request.POST:
        isproposed = False;
    elif 'propose' in request.POST:
        isproposed = True;
    try:
        new_user = User.objects.get(username="username")
    except ObjectDoesNotExist:
        new_user = User.objects.create_user(username="username", password="password1")
        new_user.save()
        
    print new_user
    #newevent = Event(user=request.user, type="attraction",proposed = isproposed)
    newevent = Event(user = new_user, type="attraction",proposed = isproposed)
    form = AttractionForm(request.POST, instance=newevent)
    print form.data['title'];
    if form.is_valid():
        form.save()
        context['success'] = 1
    else:
        context['failure'] = 1
    return render(request, 'travelpad/addevent.html', context)
 
