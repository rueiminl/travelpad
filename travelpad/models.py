from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import User 
from django.core.urlresolvers import reverse
import time

# add as_dict mthod to User
def user_as_dict(self):
    return dict(id=self.id, username=self.username, photo=reverse('get_user_photo', kwargs={'id':self.id}))
User.add_to_class("as_dict",user_as_dict)

class Itinerary(models.Model):
    created_by = models.ForeignKey(User, related_name="itineraries")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=3000, blank=True)
    place_id = models.CharField(max_length=100, blank=True)
    place_lat = models.CharField(max_length=100, blank=True)
    place_lng = models.CharField(max_length=100, blank=True)
    place_name = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    participants = models.ManyToManyField(User, blank=True)
    photo = models.FileField(upload_to="pictures", blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    def as_dict(self):
        return dict(
            id=self.id,
            created_by=self.created_by.as_dict(), 
            title=self.title,
            description=self.description, 
            place=dict(id=self.place_id, name=self.place_name, latitude=self.place_lat, longitude=self.place_lng),
            # location=self.location,
            #timezone.localtime(self.start_date).strftime("%Y-%m-%d"), Error: 'datetime.date' object has no attribute 'astimezone'
            start_date=self.start_date.isoformat(),
            end_date=self.end_date.isoformat(),#timezone.localtime(self.end_date).strftime("%Y-%m-%d"),
            participants=[user.as_dict() for user in self.participants.all()],
            # photo=self.photo, #TODO: get url
            timestamp=self.timestamp.isoformat(),
            )

class Event(models.Model):
    created_by = models.ForeignKey(User)
    type = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    note = models.CharField(max_length=60, blank=True)
    related_itinerary = models.ForeignKey(Itinerary)
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
            'start': timezone.localtime(self.start_datetime).isoformat(), #ISO8601
            'end': timezone.localtime(self.end_datetime).isoformat(),
            "place": {"id": self.place_id, "name": self.place_name, "latitude": self.place_latitude, "longitude": self.place_longitude},
            "note": self.note,
            "type": self.type,
            "proposed": self.proposed,
            "transportation": self.pre.as_dict() if hasattr(self,'pre') else 'null',
        }

        
class Transportation(models.Model):
    created_by = models.ForeignKey(User)
    type = models.CharField(max_length=30)
    note = models.CharField(max_length=60, blank=True)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    related_itinerary = models.ForeignKey(Itinerary)
    route = models.CharField(max_length=100, blank=True)
    source = models.OneToOneField(Event, related_name="pre")
    destination = models.OneToOneField(Event, related_name="next")
    timestamp = models.DateTimeField(auto_now_add=True)
    def as_dict(self):
        return {
            "id": self.id,
            "title": self.type,
            "startdate": timezone.localtime(self.start_datetime).strftime("%Y-%m-%d"),
            "starttime": timezone.localtime(self.start_datetime).strftime("%H:%M"),
            "enddate": timezone.localtime(self.end_datetime).strftime("%Y-%m-%d"),
            "endtime": timezone.localtime(self.end_datetime).strftime("%H:%M"),
            'start': timezone.localtime(self.start_datetime).isoformat(), #ISO8601
            'end': timezone.localtime(self.end_datetime).isoformat(),
            "source": self.source.place_name,
            "destination": self.destination.place_name,
            "note": self.note,
            "type": self.type,
        }

class Todo(models.Model):
    created_by = models.ForeignKey(User, related_name='created_by')
    task = models.CharField(max_length=300)
    status = models.CharField(max_length=64, default='pending', blank=True)
    related_event = models.ForeignKey(Event, blank=True,null=True)
    related_itinerary = models.ForeignKey(Itinerary)
    owner = models.ForeignKey(User, blank=True, null=True, related_name='owned_by')
    note = models.CharField(max_length=300, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    def as_dict(self):
        return dict(
            id=self.id,
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
    owner = models.ForeignKey(User, blank=True, null=True, related_name='owncost')
    note = models.CharField(max_length=300, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    creation_time = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    def as_dict(self):
    
        return {
            "id": self.id,
            "participant": [user.as_dict() for user in self.participant.all()],
            "isall": self.isall,
            "status": self.status,
            "related_event": self.related_event.title if self.related_event else '',
            "owner": self.owner.as_dict() if self.owner else '',
            "note": self.note,
            "amount": float(self.amount),
            "creation_time": self.creation_time.isoformat(),
        }

class Message(models.Model):
    content = models.CharField(max_length=160)
    created_by = models.ForeignKey(User)
    related_itinerary = models.ForeignKey(Itinerary)
    creation_time = models.DateTimeField(auto_now_add=True)    
    timestamp = models.DateTimeField(auto_now=True)
    def as_dict(self):
        return dict(
            id=self.id,
            created_by=self.created_by.as_dict(), 
            content=self.content,
            replies=[reply.as_dict() for reply in self.replies.all()] if hasattr(self,'replies') else [],
            creation_time=timezone.localtime(self.creation_time).isoformat(),
            # timestamp=timezone.localtime(self.timestamp).isoformat(),
            timestamp=int(time.mktime(self.timestamp.timetuple())*1000)
        )
        
class Reply(models.Model):
    content = models.CharField(max_length=160)
    created_by = models.ForeignKey(User)
    related_message = models.ForeignKey(Message, related_name='replies')
    creation_time = models.DateTimeField(auto_now_add=True)    
    timestamp = models.DateTimeField(auto_now=True)
    def as_dict(self):
        return dict(
            id=self.id,
            created_by=self.created_by.as_dict(), 
            related_message=self.related_message.id, 
            content=self.content,
            creation_time=timezone.localtime(self.creation_time).isoformat(),
            timestamp=timezone.localtime(self.timestamp).isoformat(),
        )

class TravelPadUser(models.Model):
	user = models.ForeignKey(User)
	photo = models.FileField(upload_to = "pictures", blank=True)



class Feedback_place(models.Model):
    created_by = models.ForeignKey(User)
    related_itinerary = models.ForeignKey(Itinerary)
    place_name = models.CharField(max_length=100,blank=True)
    place_id = models.CharField(max_length=30,blank=True)
    comment = models.CharField(max_length=3000, blank=True)
    rating = models.IntegerField()

class Photos(models.Model):
    created_by = models.ForeignKey(User)
    related_event = models.ForeignKey(Event)
    photo = models.FileField(upload_to="placeImage")
    comment = models.CharField(max_length=3000)

def create_message(instance, created, raw, **kwargs):
    # Ignore fixtures and saves for existing courses.
    if not created or raw:
        return
    if isinstance(instance, Event):
        entry = Message(
            created_by=instance.created_by, 
            related_itinerary=instance.related_itinerary,
            content='I just created a "' + instance.title + '" event!',
            )
        entry.save()
    # elif isinstance(instance, Todo):
#         entry = Message(
#             created_by=instance.created_by,
#             related_itinerary=instance.related_itinerary,
#             content=instance.created_by.username + " created " + instance.task + " task",
#             )
#         entry.save()

def update_message_timestamp(instance, created, raw, **kwargs):
    # Ignore fixtures and saves for existing courses.
    if raw:
        return
    if isinstance(instance, Reply):
        message = Message.objects.get(id=instance.related_message.id)
        message.save() #update timestamp

def update_message_timestamp(sender, instance, **kwargs):
    if isinstance(instance, Reply):
        message = Message.objects.get(id=instance.related_message.id)
        message.save() #update timestamp

models.signals.post_save.connect(create_message, sender=Event, dispatch_uid='create_message')
models.signals.post_save.connect(create_message, sender=Todo, dispatch_uid='create_message')
models.signals.post_save.connect(update_message_timestamp, sender=Reply, dispatch_uid='update_message_timestamp')
models.signals.post_delete.connect(update_message_timestamp, sender=Reply, dispatch_uid='update_message_timestamp')


