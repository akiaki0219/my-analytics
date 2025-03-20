import uuid
from django.db import models
from django.utils import timezone

class Analytic(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  videoId = models.IntegerField()
  get_at = models.DateField(default=timezone.now)
  YouTubeView = models.PositiveIntegerField()
  niconicoView = models.PositiveIntegerField()
  YouTubeLike = models.PositiveIntegerField()
  niconicoLike = models.PositiveIntegerField()
  YouTubeComment = models.PositiveIntegerField()
  niconicoComment = models.PositiveIntegerField()
  niconicoMylist = models.PositiveIntegerField()

  def totalStatistic(self):
    statistic = {
      "view": self.YouTubeView + self.niconicoView,
      "like": self.YouTubeLike + self.niconicoLike,
      "comment": self.YouTubeComment + self.niconicoComment
    }
    return statistic
