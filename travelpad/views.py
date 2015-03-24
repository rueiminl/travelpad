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
	if request.method == 'GET':
		return todolist(request)
	todo = Todo()
	form = TodoForm(request.POST, instance = todo)
	if not form.is_valid():
		return todolist(request)
	form.save()
	return todolist(request)

def update_todo(request, id):
	print "update_todo", id
	if request.method == 'GET':
		return todolist(request)
	todo = get_object_or_404(Todo, id = id)
	if not todo:
		raise Http404
	form = TodoForm(request.POST, instance = todo)
	if not form.is_valid():
		return todolist(request)
	form.save()
	return todolist(request)
