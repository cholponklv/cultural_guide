from rest_framework import serializers
from events import models

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Events
        fields = ('id','title','category','photo','description','price','date','time_start','time_end','views','priority','geolocation_name','organizer')

class CategoryEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategoryEvents
        fields = ('id','title',)

class CommentsEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentsEvents
        fields = ('id','title','events','user','created_at')

class LikesEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LikesEvents
        fields = ('id','events','user','created_at')


class LikesCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LikesComments
        fields = ('id','comments','user','created_at')