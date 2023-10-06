from django.shortcuts import render
from rest_framework import viewsets,permissions,filters
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response
from events import models
from events import serializers
from events import filter
# Create your views here.
class EventsViewSet(viewsets.ModelViewSet):
    queryset = models.Events.objects.all()
    serializer_class = serializers.EventsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (dj_filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_class = filter.EventsFilters
    ordering_fields = '__all__'
    search_fields = ('title','description', 'geolocation_name','date','time_start',"time_end")

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)