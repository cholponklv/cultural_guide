from django.shortcuts import render

# Create your views here.
from .models import User,Favourites
from rest_framework import generics, permissions,status,viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from user import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from tours.models import Tours
from events.models import Events
from eventsdate.models import Meeting
from django.shortcuts import get_object_or_404

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        refresh = RefreshToken.for_user(user)
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_object(self):
        return self.request.user


class CompanyRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.CompanyRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        refresh = RefreshToken.for_user(user)
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class FavouritesCreateView(generics.CreateAPIView):
    queryset = Favourites.objects.all()
    serializer_class = serializers.FavouritesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        type = self.request.data.get('type')

        if type == 'event':
            event_id = self.request.data.get('events')
            event = get_object_or_404(Events, pk=event_id)
            serializer.save(user=user, events=event,type=self.request.data.get('type'))
        elif type == 'tour':
            tour_id = self.request.data.get('tours')
            tour = get_object_or_404(Tours, pk=tour_id)
            serializer.save(user=user, tours=tour,type=self.request.data.get('type'))
        elif type == 'meeting':
            meeting_id = self.request.data.get('meetings')
            meeting = get_object_or_404(Meeting, pk=meeting_id)
            serializer.save(user=user, meetings=meeting,type=self.request.data.get('type'))

class FavouritesListAPIView(generics.ListAPIView):
    serializer_class = serializers.FavouritesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Favourites.objects.filter(user=user)