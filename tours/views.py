from django.shortcuts import render
from rest_framework import viewsets,permissions,filters
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response
from tours import models
from tours import serializers
from tours import filter
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
# Create your views here.
class ToursViewSet(viewsets.ModelViewSet):
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
    
class CategoryToursViewSet(viewsets.ModelViewSet):
    queryset = models.CategoryTours.objects.all()
    serializer_class = serializers.CategoryToursSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewsToursViewSet(viewsets.ModelViewSet):
    queryset = models.ReviewsTours.objects.all()
    serializer_class = serializers.ReviewsToursSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikesToursListCreateView(generics.ListCreateAPIView):
    queryset = models.LikesTours.objects.all()
    serializer_class = serializers.LikesToursSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        tour_id = self.kwargs.get('tour_id')
        tour = get_object_or_404(models.Tours, pk=tour_id)
        user = self.request.user

        existing_like = models.LikesTours.objects.filter(tours=tour, user=user).first()
        
        if existing_like:
            existing_like.delete()
            tour.likes_count -= 1
            tour.save()
        else:
            serializer.save(user=user, tours=tour)
            tour.likes_count += 1
            tour.save()
        return Response({'message': 'Лайк обновлен'}, status=status.HTTP_200_OK)

class LikesReviewsListCreateView(generics.ListCreateAPIView):
    queryset = models.LikesReviews.objects.all()
    serializer_class = serializers.LikesReviewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(models.CommentsEvents, pk=review_id)
        user = self.request.user

        existing_like = models.LikesReviews.objects.filter(reviews=review, user=user).first()
        
        if existing_like:
            existing_like.delete()
            review.likes_count -= 1
            review.save()
        else:
            serializer.save(user=user, reviews=review)
            review.likes_count += 1
            review.save()
        return Response({'message': 'Лайк обновлен'}, status=status.HTTP_200_OK)



class JoinMeetingAPIView(APIView):
    def post(self, request, tour_id):
        tour = get_object_or_404(models.Tours, pk=tour_id)
        user = request.user
        text = request.data.get('text', '')  

        existing_membertour = models.ToursMembers.objects.filter(user=user, tours = tour).first()

        if existing_membertour:
            existing_membertour.delete()
            message = 'Присоединение отменено'
        else:
            current_members_count = models.ToursMembers.objects.filter(tours=tour).count()

            if current_members_count >= tour.max_members:
                return Response({'error': 'Переполнено'}, status=status.HTTP_400_BAD_REQUEST)

            tours_member = models.ToursMembers(user=user, tours=tour, text=text)
            tours_member.save()
            message = 'Успешно присоединено'

        serializer = serializers.ToursMembersSerializer(tours_member) if 'tours_member' in locals() else None
        return Response({'message': message, 'tours_member': serializer.data if serializer else None})