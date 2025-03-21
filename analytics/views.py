from analytics.fetch import FetchAnalytics
from analytics.models import Analytic
from datetime import date
from django.http import Http404
from django.shortcuts import redirect, render

def index(request):
  sort_options = {
    'id': 'videoId',
    'view': 'YouTubeView',
    'like': 'YouTubeLike',
    'comment': 'YouTubeComment'
  }
  sort_field = sort_options.get(request.GET.get('sort'), 'videoId')
  order = '' if request.GET.get('order')=='asc' else '-'
  analytics = Analytic.objects.filter(get_at=date.today()).order_by('{}{}'.format(order, sort_field))
  context = {
    'analytics': analytics
  }
  return render(request, "analytics/index.html", context)

def detail(request, analytic_id):
  try: analytic = Analytic.objects.get(pk=analytic_id)
  except Analytic.DoesNotExist: raise Http404("Task doen not exist")
  context = {
    'analytic': analytic
  }
  return render(request, 'analytics/detail.html', context)

def fetch(request):
  if request.method == "POST":
    fetchAnalytics = FetchAnalytics()
    for fetchAnalytic in fetchAnalytics.items():
      fetchAnalyticJson = fetchAnalytic[1]
      videoId, get_at = fetchAnalyticJson['videoId'], fetchAnalyticJson['get_at']
      YouTubeView, YouTubeLike, YouTubeComment = int(fetchAnalyticJson['analytic']['view']['YouTube']), int(fetchAnalyticJson['analytic']['like']['YouTube']), int(fetchAnalyticJson['analytic']['comment']['YouTube'])
      niconicoView, niconicoLike, niconicoComment, niconicoMylist = int(fetchAnalyticJson['analytic']['view']['niconico']), int(fetchAnalyticJson['analytic']['like']['niconico']), int(fetchAnalyticJson['analytic']['comment']['niconico']), int(fetchAnalyticJson['analytic']['mylist']['niconico'])
      try:
        analytic = Analytic.objects.get(videoId=videoId, get_at=get_at)
        analytic.YouTubeView = YouTubeView
        analytic.YouTubeLike = YouTubeLike
        analytic.YouTubeComment = YouTubeComment
        analytic.niconicoView = niconicoView
        analytic.niconicoLike = niconicoLike
        analytic.niconicoComment = niconicoComment
        analytic.niconicoMylist = niconicoMylist
      except Analytic.DoesNotExist:
        analytic = Analytic(
          videoId = videoId,
          get_at = get_at,
          YouTubeView = YouTubeView,
          YouTubeLike = YouTubeLike,
          YouTubeComment = YouTubeComment,
          niconicoView = niconicoView,
          niconicoLike = niconicoLike,
          niconicoComment = niconicoComment,
          niconicoMylist = niconicoMylist
        )
      analytic.save()
    return redirect('top')
  return render(request, 'analytics/fetch.html')