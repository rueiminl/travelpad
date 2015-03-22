from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *

def todolist(request):
	todoes = Todo.objects.all()
	form = TodoForm()
	context = {'todoes' : todoes, 'form' : form}
	return render(request, 'travelpad/todolist.html', context)

def create_todo(request):
	todo = Todo()
	form = TodoForm(request.POST, instance = todo)
	if not form.is_valid():
		return todolist(request)
	form.save()
	return todolist(request)
