from analytics.fetch import FetchAnalytics
from analytics.models import Analytic
from django.http import Http404
from django.shortcuts import render

def index(request):
  if request.method == "POST":
    fetchAnalytics = FetchAnalytics()
    for i in fetchAnalytics:
      fetchAnalytic = fetchAnalytics[i]
      analytic = Analytic(
        videoId = fetchAnalytic['videoId'],
        get_at = fetchAnalytic['get_at'],
        YouTubeView = int(fetchAnalytic['analytic']['view']['YouTube']),
        YouTubeLike = int(fetchAnalytic['analytic']['like']['YouTube']),
        YouTubeComment = int(fetchAnalytic['analytic']['comment']['YouTube']),
        niconicoView = int(fetchAnalytic['analytic']['view']['niconico']),
        niconicoLike = int(fetchAnalytic['analytic']['like']['niconico']),
        niconicoComment = int(fetchAnalytic['analytic']['comment']['niconico']),
        niconicoMylist = int(fetchAnalytic['analytic']['mylist']['niconico'])
      )
      analytic.save()
  sort_options = {
    'id': 'videoId',
    'view': 'YouTubeView',
    'like': 'YouTubeLike',
    'comment': 'YouTubeComment'
  }
  sort_field = sort_options.get(request.GET.get('sort'), 'videoId')
  order = '' if request.GET.get('order')=='asc' else '-'
  analytics = Analytic.objects.order_by('{}{}'.format(order, sort_field))
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