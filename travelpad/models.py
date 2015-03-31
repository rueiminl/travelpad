from django.db import models
from django.contrib.auth.models import User
from datetime import datetime    

class Event(models.Model):
    user = models.ForeignKey(User)
    type = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    note = models.CharField(max_length=60, blank=True)
    #start_date = models.DateField()
    #start_time = models.TimeField()
    #end_date = models.DateField()
    #end_time = models.TimeField()
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    place_id = models.CharField(max_length=30,blank=True)
    place_name = models.CharField(max_length=100,blank=True)
    place_latitude = models.CharField(max_length=30,blank=True)
    place_longitude = models.CharField(max_length=30,blank=True)
    route = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=30, blank=True)
    destination = models.CharField(max_length=30, blank=True)
    proposed = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now=True)

class Itinerary(models.Model):
	timestamp = models.DateTimeField(auto_now = True)

class Todo(models.Model):
	create_by = models.ForeignKey(User)
    # created_by = models.CharField(max_length=64)
	task = models.CharField(max_length=300)
	status = models.CharField(max_length=64)
	related_event = models.ForeignKey(Event, blank=True)
    # related_event = models.CharField(max_length=64)
	related_itinerary = models.ForeignKey(Itinerary)
    # related_itinerary = models.CharField(max_length=64)
	# owner = models.ForeignKey(User, related_name="own_todoes")
	owner = models.CharField(max_length=64, blank=True)
	note = models.CharField(max_length=300, blank=True)
	timestamp = models.DateTimeField(auto_now = True)
	def __unicode__(self):
		return self.task

class Message(models.Model):
    content = models.CharField(max_length=160)
    timestamp = models.DateTimeField(auto_now=True)    
    created_by = models.ForeignKey(User)

        
        
class Reply(models.Model):
    content = models.CharField(max_length=160)
    timestamp = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    related_message = models.ForeignKey(Message)


class TravelPadUser(models.Model):
	user = models.ForeignKey(User, related_name = 'user_user')
	picture = models.FileField(upload_to = "pictures", blank = True)
	content_type = models.CharField(max_length=50, blank = True)
	def __unicode__(self):
		return self.user.username + "(" + self.user.first_name + " " + self.user.last_name + "); pic: " + self.content_type;
