from djongo import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Additional fields can be added here
    pass

class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField('User', related_name='teams')

class Activity(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    date = models.DateField()

class Workout(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()

class LeaderboardEntry(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    points = models.IntegerField()
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, blank=True)
