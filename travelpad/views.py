from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404

def todo(request):
	context = {}
	return render(request, 'travelpad/todo.html', context) 
