from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from travelpad.models import *
from travelpad.forms import *
from travelpad.forms_login import *
from travelpad.views_itinerary import demo
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

def login(request):
	todoes = Todo.objects.all()
	form = TodoForm()
	context = {'todoes' : todoes, 'form' : form}
	return render(request, 'travelpad/todolist.html', context)

@transaction.atomic
def register(request):
	context = {}
	if request.method == 'GET':
		context['form'] = RegisterForm()
		return render(request, 'travelpad/register.html', context)

	# Creates a bound form from the request POST parameters and makes the 
	# form available in the request context dictionary.
	# Validates the form.
	travelpad_user = TravelPadUser()
	form = RegisterForm(request.POST, instance = travelpad_user)

	if not form.is_valid():
		context['form'] = form
		return render(request, 'travelpad/register.html', context)
		
	# Creates the new user from the valid form data
	new_user = User.objects.create_user(username=form.cleaned_data['username'],
										first_name=form.cleaned_data['firstname'],
										last_name=form.cleaned_data['lastname'],
										password=form.cleaned_data['password1'],
										email=form.cleaned_data['email'])
	new_user.is_active = False
	new_user.save()
	
	travelpad_user.user = new_user
	form.save()
	
	token = default_token_generator.make_token(new_user)
	email_body = """
Welcome to the TravelPad.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), reverse('confirm', args=(new_user.username, token)))
	send_mail(subject="Verify your email address", message= email_body, from_email="rueiminl@andrew.cmu.edu", recipient_list=[new_user.email])
	context['email'] = form.cleaned_data['email']
	return render(request, 'travelpad/needs-confirmation.html', context)

def confirm(request, username, token):
	user = get_object_or_404(User, username=username)
	if not default_token_generator.check_token(user, token):
		raise Http404
	user.is_active = True
	user.save()
	return render(request, 'travelpad/confirmed.html', {})
