from rest_framework.routers import DefaultRouter
from django.urls import path, include
from events import views

router = DefaultRouter()

router.register('events', viewset=views.EventsViewSet, basename='events')
router.register('category', viewset=views.CategoryEventsViewSet,
                basename='category_events')

urlpatterns = [
    path('', include(router.urls)),
    path('events/<int:events_id>/likes/',
         views.LikeEventsListCreateView().as_view(), name='likes_events'),
    path('comments/<int:comment_id>/likes/',
         views.LikeCommentsListCreateView().as_view(), name='likes_comments'),
    path('events/<int:event_id>/comments/',
         views.CommentsEventsListCreateView.as_view(), name='event-comments-list'),
]
