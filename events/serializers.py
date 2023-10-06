from rest_framework import serializers
from events import models

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Events
        fields = ('id','title','category','photo','description','price','date','time_start','time_end','views','priority','geolocation_name','organizer')
