from django_filters.rest_framework import filterset
from eventsdate import models


class MeetingFilters(filterset.FilterSet):
    class Meta:
        model = models.Meeting
        fields = ('id', 'title', 'description', 'price', 'date_time',
                  'views', 'geolocation_name', 'max_members', 'organizer')
