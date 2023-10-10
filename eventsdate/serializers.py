from rest_framework import serializers
from eventsdate import models


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Meeting
        fields = ('id', 'title', 'photo', 'description', 'price', 'date_time',
                  'views', 'geolocation_name', 'max_members', 'organizer')


class MeetingMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MeetingMembers
        fields = ('text',)
