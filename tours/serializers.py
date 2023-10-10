from rest_framework import serializers
from tours import models


class ToursSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tours
        fields = ('id', 'title', 'category', 'photo', 'description', 'price', 'date', 'duration',
                  'time_start', 'time_end', 'max_members', 'views', 'geolocation_name', 'organizer')


class CategoryToursSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategoryTours
        fields = ('id', 'title',)


class ReviewsToursSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReviewsTours
        fields = ('id', 'title', 'tours', 'user', 'created_at')


class LikesToursSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LikesTours
        fields = ('id', 'tours', 'user', 'created_at')


class LikesReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LikesReviews
        fields = ('id', 'reviews', 'user', 'created_at')


class ToursMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ToursMembers
        fields = ('text',)
