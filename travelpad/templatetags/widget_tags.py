from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
import dateutil.parser
from json import dumps
import json
from django import template

register = template.Library()

#@register.simple_tag
#register.inclusion_tag('travelpad/calendar.html', calendar)
@register.inclusion_tag('travelpad/calendar.html')
def calendar(itinerary):
	return {'itinerary' : itinerary}

@register.inclusion_tag('travelpad/todolist.html')
def todolist(itinerary):
    todoes = Todo.objects.all()
    form = TodoForm()
    return {'todoes' : todoes, 'form' : form}