from django_filters.rest_framework import filterset
from tours import models

class ToursFilters(filterset.FilterSet):
    class Meta:
        model = models.Tours
        fields = ('id','title','category','description','price','date','duration','time_start','time_end','views','geolocation_name','organizer')

