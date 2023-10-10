
# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response
from eventsdate import models
from eventsdate import serializers
from eventsdate import filter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
# Create your views here.


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = models.Meeting.objects.all()
    serializer_class = serializers.MeetingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (dj_filters.DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter)
    filterset_class = filter.MeetingFilters
    ordering_fields = '__all__'
    search_fields = ('title', 'description', 'geolocation_name', 'date_time')

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class JoinMeetingAPIView(APIView):
    def post(self, request, meeting_id):
        meeting = get_object_or_404(models.Meeting, pk=meeting_id)
        user = request.user
        text = request.data.get('text', '')

        existing_membership = models.MeetingMembers.objects.filter(
            user=user, meeting=meeting).first()

        if existing_membership:
            existing_membership.delete()
            message = 'Присоединение отменено'
        else:
            current_members_count = models.MeetingMembers.objects.filter(
                meeting=meeting).count()

            if current_members_count >= meeting.max_members:
                return Response({'error': 'Переполнено'}, status=status.HTTP_400_BAD_REQUEST)

            meeting_member = models.MeetingMembers(
                user=user, meeting=meeting, text=text)
            meeting_member.save()
            message = 'Успешно присоединено'

        serializer = serializers.MeetingMembersSerializer(
            meeting_member) if 'meeting_member' in locals() else None
        return Response({'message': message, 'meeting_member': serializer.data if serializer else None})
