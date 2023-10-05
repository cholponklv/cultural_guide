from django.db import models

# Create your models here.
from django.db import models

from user.models import User
# Create your models here.


class Tours(models.Model):
    title = models.CharField(max_length=155)
    category = models.ManyToManyField('CategoryTours')
    photo = models.ImageField(upload_to='events', blank=True, null=True)
    description = models.TextField()
    price = models.IntegerField(default=0)
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    date_end = models.TimeField()
    duration = models.DurationField()
    views = models.IntegerField(default=0)
    geolocation_name = models.CharField(max_length=155)
    max_members = models.IntegerField()
    route = models.TextField()
    services_included = models.TextField(blank=True, null=True)
    organizer = models.ForeignKey(User,on_delete=models.CASCADE,default=None,related_name='organized_tours')


class ToursMembers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tours = models.ForeignKey(Tours, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} на {self.tours.title}'

    class Meta:
        unique_together = ('user', 'tours')


class CategoryTours(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return str(self.title)


class ReviewsTours(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    tours = models.ForeignKey(Tours,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class LikesTours(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tours = models.ForeignKey(Tours,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"Like by {self.user} on Event {self.tours.id}")


class LikesReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"Like by {self.user} on Reviews {self.reviewstours.id}")
