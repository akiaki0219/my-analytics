from django.db import models
from django.utils import timezone

class Analytic(models.Model):
  videoId = models.IntegerField()
  videoTitle = models.CharField(max_length=100)
  get_at = models.DateField(default=timezone.now)
  YouTubeView = models.PositiveIntegerField()
  niconicoView = models.PositiveIntegerField()
  YouTubeLike = models.PositiveIntegerField()
  niconicoLike = models.PositiveIntegerField()
  YouTubeComment = models.PositiveIntegerField()
  niconicoComment = models.PositiveIntegerField()
  niconicoMylist = models.PositiveIntegerField()