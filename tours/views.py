from django.shortcuts import render
from rest_framework import viewsets,permissions,filters
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response
from tours import models
from tours import serializers
from tours import filter
from rest_framework import generics
from django.shortcuts import get_object_or_404
# Create your views here.
class EventsViewSet(viewsets.ModelViewSet):
    queryset = models.Tours.objects.all()
    serializer_class = serializers.ToursSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (dj_filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_class = filter.ToursFilters
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
    
class CategoryEventsViewSet(viewsets.ModelViewSet):
    queryset = models.CategoryEvents.objects.all()
    serializer_class = serializers.CategoryEventsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentsEventsViewSet(viewsets.ModelViewSet):
    queryset = models.CommentsEvents.objects.all()
    serializer_class = serializers.CommentsEventsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeEventsListCreateView(generics.ListCreateAPIView):
    queryset = models.LikesEvents.objects.all()
    serializer_class = serializers.LikesEventsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        event_id = self.kwargs.get('events_id')
        events = get_object_or_404(models.Events, pk=event_id)
        user = self.request.user

        existing_like = models.LikesEvents.objects.filter(events=events, user=user).first()
        
        if existing_like:
            existing_like.delete()
        else:
            serializer.save(user=user, events=events)

class LikeCommentsListCreateView(generics.ListCreateAPIView):
    queryset = models.LikesComments.objects.all()
    serializer_class = serializers.LikesCommentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment_id = self.kwargs.get('comment_id')
        comments = get_object_or_404(models.CommentsEvents, pk=comment_id)
        user = self.request.user

        existing_like = models.LikesComments.objects.filter(comments=comments, user=user).first()
        
        if existing_like:
            existing_like.delete()
        else:
            serializer.save(user=user, comments=comments)