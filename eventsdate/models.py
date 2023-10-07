from django.db import models
from user.models import User
# Create your models here.


class Meeting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    geolocation_name = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    photo = models.ImageField(upload_to='meeting', blank=True, null=True)
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='organized_events')
    max_members = models.PositiveIntegerField()
    views = models.IntegerField(default=0)
    price = models.IntegerField()

    def __str__(self):
        return self.title


class MeetingMembers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'{self.user.username} на {self.meeting.title}'

    class Meta:
        unique_together = ('user', 'meeting')
