from django.db import models
from django.contrib.auth.models import User
from datetime import datetime    

class Event(models.Model):
    user = models.ForeignKey(User)
    type = models.CharField(max_length=10)
    title = models.CharField(max_length=30)
    note = models.CharField(max_length=60, blank=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    place_id = models.CharField(max_length=30, blank=True)
    place_name = models.CharField(max_length=30, blank=True)
    place_latitude = models.CharField(max_length=30, blank=True)
    place_longitude = models.CharField(max_length=30, blank=True)
    route = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=30, blank=True)
    destination = models.CharField(max_length=30, blank=True)
    proposed = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add=True)

class Itinerary(models.Model):
	timestamp = models.DateTimeField(auto_now_add = True)

class Todo(models.Model):
	# create_by = models.ForeignKey(User, related_name="create_todoes")
	created_by = models.CharField(max_length=64)
	task = models.CharField(max_length=300)
	status = models.CharField(max_length=64)
	# related_event = models.ForeignKey(Event)
	related_event = models.CharField(max_length=64)
	# related_itinerary = models.ForeignKey(Itinerary)
	related_itinerary = models.CharField(max_length=64)
	# owner = models.ForeignKey(User, related_name="own_todoes")
	owner = models.CharField(max_length=64)
	note = models.CharField(max_length=300)
	timestamp = models.DateTimeField(auto_now_add = True)
	def __unicode__(self):
		return self.task

