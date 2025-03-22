import uuid
from datetime import date
from django.db import models
from django.utils import timezone

class Video(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  video_number: int = models.IntegerField(unique=True)
  title: str = models.CharField(max_length=100, default="title")
  posted_at: date = models.DateField()
  YouTube: str = models.CharField(max_length=11, null=True, blank=True)
  niconico: str = models.CharField(max_length=11, null=True, blank=True)

class Analytic(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  video: Video = models.ForeignKey(Video, on_delete=models.DO_NOTHING)
  get_at: date = models.DateField(default=timezone.now)
  YouTubeView: int = models.PositiveIntegerField(default=0)
  niconicoView: int = models.PositiveIntegerField(default=0)
  YouTubeLike: int = models.PositiveIntegerField(default=0)
  niconicoLike: int = models.PositiveIntegerField(default=0)
  YouTubeComment: int = models.PositiveIntegerField(default=0)
  niconicoComment: int = models.PositiveIntegerField(default=0)
  niconicoMylist: int = models.PositiveIntegerField(default=0)

  def totalStatistic(self):
    statistic = {
      "view": self.YouTubeView + self.niconicoView,
      "like": self.YouTubeLike + self.niconicoLike,
      "comment": self.YouTubeComment + self.niconicoComment
    }
    return statistic

def compareAnalytic(analytic1: Analytic, analytic2: Analytic):
  analytic1_totalStatistics, analytic2_totalStatistics = analytic1.totalStatistic(), analytic2.totalStatistic()
  return {
      "view": {
        "YouTube": analytic1.YouTubeView-analytic2.YouTubeView,
        "niconico": analytic1.niconicoView-analytic2.niconicoView,
        "total": analytic1_totalStatistics["view"]-analytic2_totalStatistics["view"]
      },
      "like": {
        "YouTube": analytic1.YouTubeLike-analytic2.YouTubeLike,
        "niconico": analytic1.niconicoLike-analytic2.niconicoLike,
        "total": analytic1_totalStatistics["like"]-analytic2_totalStatistics["like"]
      },
      "comment": {
        "YouTube": analytic1.YouTubeComment-analytic2.YouTubeComment,
        "niconico": analytic1.niconicoComment-analytic2.niconicoComment,
        "total": analytic1_totalStatistics["comment"]-analytic2_totalStatistics["comment"]
      },
      "mylist": {
        "niconico": analytic1.niconicoMylist-analytic2.niconicoMylist
      }
    }