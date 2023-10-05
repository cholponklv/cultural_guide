from django.db import models
from user.models import User
# Create your models here.


class Meeting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    geolocation_name = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='organized_events')
    members = models.ManyToManyField(
        User, through='MeetingMembers')
    max_members = models.PositiveIntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.name


class MeetingMembers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} на {self.meeting.title}'

    class Meta:
        unique_together = ('user', 'meeting')
