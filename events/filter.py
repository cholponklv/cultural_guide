from django_filters.rest_framework import filterset
from events import models


class EventsFilters(filterset.FilterSet):
    class Meta:
        model = models.Events
        fields = ('id', 'title', 'category__title', 'description', 'price', 'date',
                  'time_start', 'time_end', 'views', 'priority', 'geolocation_name', 'organizer')
