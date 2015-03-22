from django.db import models
from django.contrib.auth.models import User
class Event(models.Model):
	timestamp = models.DateTimeField(auto_now_add = True)

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

