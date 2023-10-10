from rest_framework.routers import DefaultRouter
from django.urls import path, include
from tours import views

router = DefaultRouter()

router.register('tours', viewset=views.ToursViewSet, basename='tours')
router.register('category', viewset=views.CategoryToursViewSet,
                basename='category_events')
router.register('reviews', viewset=views.ReviewsToursViewSet,
                basename='reviews_tours')

urlpatterns = [
    path('', include(router.urls)),
    path('tours/<int:tour_id>/likes/',
         views.LikesToursListCreateView().as_view(), name='likes_tours'),
    path('reviews/<int:review_id>/likes/',
         views.LikesReviewsListCreateView().as_view(), name='likes_comments'),
    path('tours/<int:tour_id>/join/',
         views.JoinMeetingAPIView.as_view(), name='join_tours_api'),
]
