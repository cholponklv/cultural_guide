
# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets,permissions,filters
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response
from eventsdate import models
from eventsdate import serializers
from eventsdate import filter
# Create your views here.
class MeetingViewSet(viewsets.ModelViewSet):
    queryset = models.Meeting.objects.all()
    serializer_class = serializers.MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (dj_filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_class = filter.MeetingFilters 
    ordering_fields = '__all__'
    search_fields = ('title','description', 'geolocation_name','date_time')

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)