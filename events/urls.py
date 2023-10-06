from rest_framework.routers import DefaultRouter
from django.urls import path, include
from events import views

router = DefaultRouter()

router.register('events', viewset=views.EventsViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
]