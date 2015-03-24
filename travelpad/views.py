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

@transaction.atomic
def create_todo(request):
	if request.method == 'GET':
		return todolist(request)
	todo = Todo()
	form = TodoForm(request.POST, instance = todo)
	if not form.is_valid():
		return todolist(request)
	form.save()
	return todolist(request)

@transaction.atomic
def update_todo(request, id):
	if request.method == 'GET':
		return todolist(request)
	todo = get_object_or_404(Todo, id=id)
	if not todo:
		raise Http404
	form = TodoForm(request.POST, instance = todo)
	if not form.is_valid():
		return todolist(request)
	form.save()
	return todolist(request)

@transaction.atomic
def delete_todo(request, id):
	todo = get_object_or_404(Todo, id=id)
	if not todo:
		raise Http404
	todo.delete()
	return todolist(request)

def add_todo_dlg(request):
	todo = Todo(task="123", status="456")
	form = TodoForm(instance = todo)
	context = {'form' : form}
	return render(request, 'travelpad/todo_dlg.html', context)

def update_todo_dlg(request, id):
	todo = get_object_or_404(Todo, id=id)
	if not todo:
		raise Http404
	form = TodoForm(instance = todo)
	context = {'id' : id, 'form' : form}
	return render(request, 'travelpad/todo_dlg.html', context)
