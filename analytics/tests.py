from analytics.models import Analytic
from datetime import date
from django.test import TestCase, Client


class SampleTestCase(TestCase):
  def test_sample1(self):
    self.assertEqual(1+2, 3)


class AnalyticModelTestCase(TestCase):
  def test_create_analytic0(self):
    get = date.today()
    analytic = Analytic(videoId=0, get_at=get, YouTubeView=0, YouTubeLike=0, YouTubeComment=0, niconicoView=0, niconicoLike=0, niconicoComment=0, niconicoMylist=0)
    analytic.save()
    analytic = Analytic.objects.get(pk=analytic.pk)
    self.assertEqual(analytic.videoId, 0)
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
    analytic = Analytic(videoId=1, get_at=get, YouTubeView=10, YouTubeLike=10, YouTubeComment=10, niconicoView=10, niconicoLike=10, niconicoComment=10, niconicoMylist=10)
    analytic.save()
    analytic = Analytic.objects.get(pk=analytic.pk)
    self.assertEqual(analytic.videoId, 1)
    self.assertEqual(analytic.get_at, get)
    self.assertEqual(analytic.YouTubeView, 10)
    self.assertEqual(analytic.YouTubeLike, 10)
    self.assertEqual(analytic.YouTubeComment, 10)
    self.assertEqual(analytic.niconicoView, 10)
    self.assertEqual(analytic.niconicoLike, 10)
    self.assertEqual(analytic.niconicoComment, 10)
    self.assertEqual(analytic.niconicoMylist, 10)

  def test_totalStatistics0(self):
    get = date.today()
    analytic = Analytic(videoId=0, get_at=get, YouTubeView=0, YouTubeLike=0, YouTubeComment=0, niconicoView=0, niconicoLike=0, niconicoComment=0, niconicoMylist=0)
    analytic.save()
    self.assertEqual(analytic.totalStatistic()["view"], 0)
    self.assertEqual(analytic.totalStatistic()["like"], 0)
    self.assertEqual(analytic.totalStatistic()["comment"], 0)

  def test_totalStatistics1(self):
    get = date.today()
    analytic = Analytic(videoId=1, get_at=get, YouTubeView=10, YouTubeLike=10, YouTubeComment=10, niconicoView=10, niconicoLike=10, niconicoComment=10, niconicoMylist=10)
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

  def test_index_get_order_id(self):
    analytic1 = Analytic(videoId=0, get_at=date.today(), YouTubeView=20, YouTubeLike=20, YouTubeComment=40, niconicoView=40, niconicoLike=60, niconicoComment=60, niconicoMylist=80)
    analytic1.save()
    analytic2 = Analytic(videoId=1, get_at=date.today(), YouTubeView=10, YouTubeLike=30, YouTubeComment=30, niconicoView=50, niconicoLike=50, niconicoComment=70, niconicoMylist=70)
    analytic2.save()
    client = Client()
    response = client.get('/?order=id')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'analytics/index.html')
    self.assertEqual(response.context["analytics"][0], analytic2)
    self.assertEqual(response.context["analytics"][1], analytic1)

  def test_index_get_order_view(self):
    analytic1 = Analytic(videoId=0, get_at=date.today(), YouTubeView=20, YouTubeLike=20, YouTubeComment=40, niconicoView=40, niconicoLike=60, niconicoComment=60, niconicoMylist=80)
    analytic1.save()
    analytic2 = Analytic(videoId=1, get_at=date.today(), YouTubeView=10, YouTubeLike=30, YouTubeComment=30, niconicoView=50, niconicoLike=50, niconicoComment=70, niconicoMylist=70)
    analytic2.save()
    client = Client()
    response = client.get('/?order=view')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'analytics/index.html')
    self.assertEqual(response.context["analytics"][0], analytic1)
    self.assertEqual(response.context["analytics"][1], analytic2)

  def test_index_get_order_like(self):
    analytic1 = Analytic(videoId=0, get_at=date.today(), YouTubeView=20, YouTubeLike=20, YouTubeComment=40, niconicoView=40, niconicoLike=60, niconicoComment=60, niconicoMylist=80)
    analytic1.save()
    analytic2 = Analytic(videoId=1, get_at=date.today(), YouTubeView=10, YouTubeLike=30, YouTubeComment=30, niconicoView=50, niconicoLike=50, niconicoComment=70, niconicoMylist=70)
    analytic2.save()
    client = Client()
    response = client.get('/?order=like')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'analytics/index.html')
    self.assertEqual(response.context["analytics"][0], analytic2)
    self.assertEqual(response.context["analytics"][1], analytic1)

  def test_index_get_order_comment(self):
    analytic1 = Analytic(videoId=0, get_at=date.today(), YouTubeView=20, YouTubeLike=20, YouTubeComment=40, niconicoView=40, niconicoLike=60, niconicoComment=60, niconicoMylist=80)
    analytic1.save()
    analytic2 = Analytic(videoId=1, get_at=date.today(), YouTubeView=10, YouTubeLike=30, YouTubeComment=30, niconicoView=50, niconicoLike=50, niconicoComment=70, niconicoMylist=70)
    analytic2.save()
    client = Client()
    response = client.get('/?order=comment')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'analytics/index.html')
    self.assertEqual(response.context["analytics"][0], analytic1)
    self.assertEqual(response.context["analytics"][1], analytic2)

  def test_detail_get_success(self):
    analytic = Analytic(videoId=0, get_at=date.today(), YouTubeView=0, YouTubeLike=0, YouTubeComment=0, niconicoView=0, niconicoLike=0, niconicoComment=0, niconicoMylist=0)
    analytic.save()
    client = Client()
    response = client.get('/{}'.format(analytic.pk))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'analytics/detail.html')
    self.assertEqual(response.context["analytic"], analytic)

  def test_detail_get_fail(self):
    client = Client()
    response = client.get('/1')
    self.assertEqual(response.status_code, 404)