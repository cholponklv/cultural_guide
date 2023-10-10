from django.db import models
from user.models import User
# Create your models here.


class Events(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'high'),
        ('low', 'low')
    ]
    title = models.CharField(max_length=155)
    category = models.ManyToManyField('CategoryEvents')
    photo = models.ImageField(upload_to='events', blank=True, null=True)
    description = models.TextField()
    price = models.IntegerField(default=0)
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    views = models.IntegerField(default=0)
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES)
    geolocation_name = models.CharField(max_length=155)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    likes_count = models.IntegerField(default=0)


class CategoryEvents(models.Model):
    title = models.CharField(max_length=155)

    def __str__(self):
        return str(self.title)


class CommentsEvents(models.Model):
    user = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, default=None)
    events = models.ForeignKey(Events, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=155)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)


class LikesEvents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    events = models.ForeignKey(
        Events, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"Like by {self.user} on Event {self.events.id}")


class LikesComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    comments = models.ForeignKey(
        CommentsEvents, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"Like by {self.user} on Event {self.commentsevents.id}")
