import dotenv
import os
from analytics.models import Analytic, Video, compareAnalytic
from datetime import date
from dateutil.relativedelta import relativedelta
from django.test import TestCase, Client
from supabase import create_client

dotenv.load_dotenv()
DEVELOPER_KEY = os.getenv("YOUTUBE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class VideoModelTestCase(TestCase):
    def test_create_video(self):
        post = date.today()
        video = Video.objects.create(video_number=1, title="test", posted_at=post, YouTube="aaaaaaaaaaa", niconico="sm9")
        video = Video.objects.get(pk=video.pk)
        self.assertEqual(video.video_number, 1)
        self.assertEqual(video.title, "test")
        self.assertEqual(video.posted_at, post)
        self.assertEqual(video.YouTube, "aaaaaaaaaaa")
        self.assertEqual(video.niconico, "sm9")
 
 
class AnalyticModelTestCase(TestCase):
    def test_create_analytic0(self):
        post, get = date.today(), date.today()
        video = Video.objects.create(video_number=1, title="test", posted_at=post, YouTube="aaaaaaaaaaa", niconico="sm9")
        analytic = Analytic.objects.create(video=video, get_at=get, YouTubeView=0, YouTubeLike=0, YouTubeComment=0, niconicoView=0, niconicoLike=0, niconicoComment=0, niconicoMylist=0)
        analytic = Analytic.objects.get(pk=analytic.pk)
        self.assertEqual(analytic.video, video)
        self.assertEqual(analytic.get_at, get)
        self.assertEqual(analytic.YouTubeView, 0)
        self.assertEqual(analytic.YouTubeLike, 0)
        self.assertEqual(analytic.YouTubeComment, 0)
        self.assertEqual(analytic.niconicoView, 0)
        self.assertEqual(analytic.niconicoLike, 0)
        self.assertEqual(analytic.niconicoComment, 0)
        self.assertEqual(analytic.niconicoMylist, 0)

    def test_create_analytic1(self):
        post, get = date.today(), date.today()
        video = Video.objects.create(video_number=1, title="test", posted_at=post, YouTube="aaaaaaaaaaa", niconico="sm9")
        analytic = Analytic.objects.create(video=video, get_at=get, YouTubeView=10, YouTubeLike=10, YouTubeComment=10, niconicoView=10, niconicoLike=10, niconicoComment=10, niconicoMylist=10)
        analytic = Analytic.objects.get(pk=analytic.pk)
        self.assertEqual(analytic.video, video)
        self.assertEqual(analytic.get_at, get)
        self.assertEqual(analytic.YouTubeView, 10)
        self.assertEqual(analytic.YouTubeLike, 10)
        self.assertEqual(analytic.YouTubeComment, 10)
        self.assertEqual(analytic.niconicoView, 10)
        self.assertEqual(analytic.niconicoLike, 10)
        self.assertEqual(analytic.niconicoComment, 10)
        self.assertEqual(analytic.niconicoMylist, 10)

    def test_totalStatistics0(self):
        post, get = date.today(), date.today()
        video = Video.objects.create(video_number=1, title="test", posted_at=post, YouTube="aaaaaaaaaaa", niconico="sm9")
        analytic = Analytic.objects.create(video=video, get_at=get, YouTubeView=0, YouTubeLike=0, YouTubeComment=0, niconicoView=0, niconicoLike=0, niconicoComment=0, niconicoMylist=0)
        self.assertEqual(analytic.totalStatistic()["view"], 0)
        self.assertEqual(analytic.totalStatistic()["like"], 0)
        self.assertEqual(analytic.totalStatistic()["comment"], 0)

    def test_totalStatistics1(self):
        post, get = date.today(), date.today()
        video = Video.objects.create(video_number=1, title="test", posted_at=post, YouTube="aaaaaaaaaaa", niconico="sm9")
        analytic = Analytic.objects.create(video=video, get_at=get, YouTubeView=10, YouTubeLike=10, YouTubeComment=10, niconicoView=10, niconicoLike=10, niconicoComment=10, niconicoMylist=10)
        self.assertEqual(analytic.totalStatistic()["view"], 20)
        self.assertEqual(analytic.totalStatistic()["like"], 20)
        self.assertEqual(analytic.totalStatistic()["comment"], 20)


class CompareAnalyticFunctionTestCase(TestCase):
    def test_compareAnalytic0(self):
        post, get = date.today(), date.today()
        video = Video.objects.create(video_number=1, title="test", posted_at=post, YouTube="aaaaaaaaaaa", niconico="sm9")
        analytic0 = Analytic.objects.create(video=video, get_at=get, YouTubeView=3, YouTubeLike=2, YouTubeComment=1, niconicoView=4, niconicoLike=7, niconicoComment=6, niconicoMylist=5)
        analytic1 = Analytic.objects.create(video=video, get_at=get, YouTubeView=0, YouTubeLike=3, YouTubeComment=2, niconicoView=5, niconicoLike=4, niconicoComment=7, niconicoMylist=6)
        comparedStats = compareAnalytic(analytic0, analytic1)
        self.assertEqual(comparedStats["view"]["YouTube"], 3)
        self.assertEqual(comparedStats["view"]["niconico"], -1)
        self.assertEqual(comparedStats["like"]["YouTube"], -1)
        self.assertEqual(comparedStats["like"]["niconico"], 3)
        self.assertEqual(comparedStats["comment"]["YouTube"], -1)
        self.assertEqual(comparedStats["comment"]["niconico"], -1)
        self.assertEqual(comparedStats["mylist"]["niconico"], -1)

    def test_compareAnalytic1(self):
        post, get = date.today(), date.today()
        video = Video.objects.create(video_number=1, title="test", posted_at=post, YouTube="aaaaaaaaaaa", niconico="sm9")
        analytic0 = Analytic.objects.create(video=video, get_at=get, YouTubeView=3, YouTubeLike=2, YouTubeComment=1, niconicoView=4, niconicoLike=7, niconicoComment=6, niconicoMylist=5)
        analytic1 = Analytic.objects.create(video=video, get_at=get, YouTubeView=0, YouTubeLike=3, YouTubeComment=2, niconicoView=5, niconicoLike=4, niconicoComment=7, niconicoMylist=6)
        comparedStats = compareAnalytic(analytic1, analytic0)
        self.assertEqual(comparedStats["view"]["YouTube"], -3)
        self.assertEqual(comparedStats["view"]["niconico"], 1)
        self.assertEqual(comparedStats["like"]["YouTube"], 1)
        self.assertEqual(comparedStats["like"]["niconico"], -3)
        self.assertEqual(comparedStats["comment"]["YouTube"], 1)
        self.assertEqual(comparedStats["comment"]["niconico"], 1)
        self.assertEqual(comparedStats["mylist"]["niconico"], 1)


class AnalyticsViewTestCase(TestCase):
    def test_index_get0(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'analytics/index.html')
        self.assertEqual(response.context["status"], "Not fetched")
        self.assertEqual(len(response.context["query_strings"]), 7)
        self.assertEqual(response.context["query_strings"]["sort"], None)
        self.assertEqual(response.context["query_strings"]["sort_option"], None)
        self.assertEqual(response.context["query_strings"]["order"], None)
        self.assertEqual(response.context["query_strings"]["compare"], None)
        self.assertEqual(response.context["query_strings"]["non_zero"], None)
        self.assertEqual(response.context["query_strings"]["non_zero_target"], None)
        self.assertEqual(response.context["query_strings"]["non_zero_option"], None)
        self.assertEqual(len(response.context["list_get_at"]), 0)
        self.assertEqual(len(response.context["analytics"]), 0)

    def test_detail_get_success0(self):
        video = Video.objects.create(video_number=1, title="test", posted_at=date.today(), YouTube="aaaaaaaaaaa", niconico="sm0")
        client = Client()
        response = client.get('/video/{}/'.format(video.video_number))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'analytics/detail.html')
        self.assertEqual(response.context["video"], video)
        self.assertEqual(len(response.context["analytics"]), 0)

    def test_detail_get_fail(self):
        client = Client()
        response = client.get('/video/{}/'.format(1))
        self.assertEqual(response.status_code, 404)

    def test_fetch_get(self):
        client = Client()
        response = client.get('/fetch/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'analytics/fetch.html')

    def test_fetch_post0(self):
        client = Client()
        response = client.post('/fetch/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/top/')

    def test_fetch_post1(self):
        supabaseClient = create_client(SUPABASE_URL, SUPABASE_KEY)
        videoList = supabaseClient.table('video').select('id, title, posted_at, YouTube, niconico').eq('public', True).execute().data
        client = Client()
        response = client.post('/fetch/')
        response = client.get('/top/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'analytics/index.html')
        self.assertEqual(response.context["status"], "Have fetched")
        self.assertEqual(len(response.context["query_strings"]), 7)
        self.assertEqual(response.context["query_strings"]["sort"], None)
        self.assertEqual(response.context["query_strings"]["sort_option"], None)
        self.assertEqual(response.context["query_strings"]["order"], None)
        self.assertEqual(response.context["query_strings"]["compare"], None)
        self.assertEqual(response.context["query_strings"]["non_zero"], None)
        self.assertEqual(response.context["query_strings"]["non_zero_target"], None)
        self.assertEqual(response.context["query_strings"]["non_zero_option"], None)
        self.assertEqual(len(response.context["list_get_at"]), 1)
        self.assertEqual(len(response.context["analytics"]), len(videoList))
