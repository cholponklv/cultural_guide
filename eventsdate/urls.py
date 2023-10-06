from rest_framework.routers import DefaultRouter
from django.urls import path, include
from eventsdate import views

router = DefaultRouter()

router.register('meetings', viewset=views.MeetingViewSet, basename='meetings')

urlpatterns = [
    path('', include(router.urls)),
]