from analytics.models import Analytic
from datetime import date
from django.test import TestCase, Client


class SampleTestCase(TestCase):
  def test_sample1(self):
    self.assertEqual(1+2, 3)


class AnalyticModelTestCase(TestCase):
  def test_create_analytic0(self):
    get = date.today()
    analytic = Analytic(videoId=0, videoTitle="analytic0", get_at=get, YouTubeView=0, YouTubeLike=0, YouTubeComment=0, niconicoView=0, niconicoLike=0, niconicoComment=0, niconicoMylist=0)
    analytic.save()
    analytic = Analytic.objects.get(pk=analytic.pk)
    self.assertEqual(analytic.videoId, 0)
    self.assertEqual(analytic.videoTitle, "analytic0")
    self.assertEqual(analytic.get_at, get)
    self.assertEqual(analytic.YouTubeView, 0)
    self.assertEqual(analytic.YouTubeLike, 0)
    self.assertEqual(analytic.YouTubeComment, 0)
    self.assertEqual(analytic.niconicoView, 0)
    self.assertEqual(analytic.niconicoLike, 0)
    self.assertEqual(analytic.niconicoComment, 0)
    self.assertEqual(analytic.niconicoMylist, 0)

  def test_create_analytic1(self):
    get = date.today()
    analytic = Analytic(videoId=1, videoTitle="analytic1", get_at=get, YouTubeView=10, YouTubeLike=10, YouTubeComment=10, niconicoView=10, niconicoLike=10, niconicoComment=10, niconicoMylist=10)
    analytic.save()
    analytic = Analytic.objects.get(pk=analytic.pk)
    self.assertEqual(analytic.videoId, 0)
    self.assertEqual(analytic.videoTitle, "analytic0")
    self.assertEqual(analytic.get_at, get)
    self.assertEqual(analytic.YouTubeView, 0)
    self.assertEqual(analytic.YouTubeLike, 0)
    self.assertEqual(analytic.YouTubeComment, 0)
    self.assertEqual(analytic.niconicoView, 0)
    self.assertEqual(analytic.niconicoLike, 0)
    self.assertEqual(analytic.niconicoComment, 0)
    self.assertEqual(analytic.niconicoMylist, 0)

  def test_totalStatistics0(self):
    get = date.today()
    analytic = Analytic(videoId=0, videoTitle="analytic0", get_at=get, YouTubeView=0, YouTubeLike=0, YouTubeComment=0, niconicoView=0, niconicoLike=0, niconicoComment=0, niconicoMylist=0)
    analytic.save()
    self.assertEqual(analytic.totalStatistic()["view"], 0)
    self.assertEqual(analytic.totalStatistic()["like"], 0)
    self.assertEqual(analytic.totalStatistic()["comment"], 0)

  def test_create_analytic1(self):
    get = date.today()
    analytic = Analytic(videoId=1, videoTitle="analytic1", get_at=get, YouTubeView=10, YouTubeLike=10, YouTubeComment=10, niconicoView=10, niconicoLike=10, niconicoComment=10, niconicoMylist=10)
    analytic.save()
    self.assertEqual(analytic.totalStatistic()["view"], 20)
    self.assertEqual(analytic.totalStatistic()["like"], 20)
    self.assertEqual(analytic.totalStatistic()["comment"], 20)


class AnalyticsViewTestCase(TestCase):
  def test_index_get(self):
    client = Client()
    response = client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'analytics/index.html')
    self.assertEqual(len(response.context["analytics"]), 0)
  
  def test_index_post(self):
    client = Client()
    data = {
      "videoId": 0,
      "videoTitle": 'test',
      "YouTubeView": 0,
      "niconicoView": 0,
      "YouTubeLike": 0,
      "niconicoLike": 0,
      "YouTubeComment": 0,
      "niconicoComment": 0,
      "niconicoMylist": 0
    }
    response = client.post('/', data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'analytics/index.html')
    self.assertEqual(len(response.context["analytics"]), 1)