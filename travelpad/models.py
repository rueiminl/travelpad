from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import User 

# add as_dict mthod to User
def as_dict(self):
    return dict(id=self.id, username=self.username)
User.add_to_class("as_dict",as_dict)

class Itinerary(models.Model):
	created_by = models.ForeignKey(User, related_name="itineraries")
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=3000, blank=True)
	location = models.CharField(max_length=100, blank=True)
	start_date = models.DateField()
	end_date = models.DateField()
	participants = models.ManyToManyField(User, blank=True)
	photo = models.FileField(upload_to="pictures", blank=True)
	timestamp = models.DateTimeField(auto_now=True)

class Event(models.Model):
    user = models.ForeignKey(User)
    type = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    note = models.CharField(max_length=60, blank=True)
    related_itinerary = models.ForeignKey(Itinerary)
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
    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "startdate": timezone.localtime(self.start_datetime).strftime("%Y-%m-%d"),
            "starttime": timezone.localtime(self.start_datetime).strftime("%H:%M"),
            "enddate": timezone.localtime(self.end_datetime).strftime("%Y-%m-%d"),
            "endtime": timezone.localtime(self.end_datetime).strftime("%H:%M"),
            "place": self.place_name,
            "note": self.note,
            "type": self.type,
            #"time": timezone.localtime(self.time).strftime("%b. %d, %Y, %I:%M %p"),
        }
        
class Transportation(models.Model):
    user = models.ForeignKey(User)
    type = models.CharField(max_length=30)
    note = models.CharField(max_length=60, blank=True)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    route = models.CharField(max_length=100, blank=True)
    source = models.OneToOneField(Event, related_name="pre")
    destination = models.OneToOneField(Event, related_name="next")
    timestamp = models.DateTimeField(auto_now_add=True)
    def as_dict(self):
        return {
            "id": self.id,
            "startdate": timezone.localtime(self.start_datetime).strftime("%Y-%m-%d"),
            "starttime": timezone.localtime(self.start_datetime).strftime("%H:%M"),
            "enddate": timezone.localtime(self.end_datetime).strftime("%Y-%m-%d"),
            "endtime": timezone.localtime(self.end_datetime).strftime("%H:%M"),
            "source": self.source.place_name,
            "destination": self.destination.place_name,
            "note": self.note,
            "type": self.type,
        }

class Todo(models.Model):
    created_by = models.ForeignKey(User, related_name='created_by')
    task = models.CharField(max_length=300)
    status = models.CharField(max_length=64)
    related_event = models.ForeignKey(Event, blank=True,null=True)
    related_itinerary = models.ForeignKey(Itinerary)
    owner = models.ForeignKey(User, blank=True, null=True, related_name='owned_by')
    note = models.CharField(max_length=300, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    #TODO:
    def as_dict(self):
        return dict(
            created_by=self.created_by.as_dict(), 
            task=self.task,
            status=self.status, 
            owner=self.owner.as_dict() if self.owner else 'null', 
            note=self.note,
            creation_time=self.creation_time.isoformat(),
            timestamp=self.timestamp.isoformat(),
        )
    
class Cost(models.Model):
    created_by = models.ForeignKey(User,related_name="creatcost")
    participant = models.ManyToManyField(User, blank=True, related_name="partcost")
    isall = models.BooleanField(default=False)
    status = models.CharField(max_length=64)
    related_event = models.ForeignKey(Event, blank=True,null=True)
    related_itinerary = models.ForeignKey(Itinerary)
    owner = models.CharField(max_length=64, blank=True)
    note = models.CharField(max_length=300, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    creation_time = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

class Message(models.Model):
    content = models.CharField(max_length=160)
    created_by = models.ForeignKey(User)
    related_itinerary = models.ForeignKey(Itinerary)
    creation_time = models.DateTimeField(auto_now_add=True)    
    timestamp = models.DateTimeField(auto_now=True)

        
        
class Reply(models.Model):
    content = models.CharField(max_length=160)
    created_by = models.ForeignKey(User)
    related_message = models.ForeignKey(Message)
    creation_time = models.DateTimeField(auto_now_add=True)    
    timestamp = models.DateTimeField(auto_now=True)


class TravelPadUser(models.Model):
	user = models.ForeignKey(User)
	photo = models.FileField(upload_to = "pictures", blank=True)
