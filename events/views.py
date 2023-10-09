from django.shortcuts import render
from rest_framework import viewsets,permissions,filters
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response
from events import models
from events import serializers
from events import filter
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404
# Create your views here.
class EventsViewSet(viewsets.ModelViewSet):
    queryset = models.Events.objects.all()
    serializer_class = serializers.EventsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    
class CategoryEventsViewSet(viewsets.ModelViewSet):
    queryset = models.CategoryEvents.objects.all()
    serializer_class = serializers.CategoryEventsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentsEventsListCreateView(generics.ListCreateAPIView):
    queryset = models.CommentsEvents.objects.all()
    serializer_class = serializers.CommentsEventsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        event_id = self.kwargs['event_id']
        
        event = get_object_or_404(models.Events, pk=event_id)
        print(event)
        serializer.save(user=self.request.user, events=event)

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        event = get_object_or_404(models.Events, pk=event_id)
        
    
        queryset = models.CommentsEvents.objects.filter(events=event)
        
        return queryset
    

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
            events.likes_count -= 1
            events.save()
        else:
            serializer.save(user=user, events=events)
            events.likes_count += 1
            events.save()
        return Response({'message': 'Лайк обновлен'}, status=status.HTTP_200_OK)


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
            comments.likes_count -= 1
            comments.save()
        else:
            serializer.save(user=user, comments=comments)
            comments.likes_count += 1
            comments.save()
        return Response({'message': 'Лайк обновлен'}, status=status.HTTP_200_OK)
