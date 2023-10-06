from rest_framework import serializers
from eventsdate import models

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Meeting
        fields = ('id','title','photo','description','price','date','time_start','time_end','views','priority','geolocation_name','organizer')
