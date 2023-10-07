from rest_framework import serializers
from tours import models

class ToursSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tours
        fields = ('id','title','category','photo','description','price','date','duration','time_start','time_end','date_end','views','priority','geolocation_name','organizer')

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