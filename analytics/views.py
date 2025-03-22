import re
from analytics.fetch import FetchAnalytics
from analytics.models import Analytic, Video, compareAnalytic
from datetime import date
from django.http import Http404
from django.shortcuts import redirect, render

def index(request):
  analytics = Analytic.objects.filter(get_at=date.today()).order_by('video__video_number')
  list_get_at = []
  if len(analytics) != 0:
    for analytic in Analytic.objects.filter(video=Video.objects.get(video_number=analytics[0].video.video_number)):
      list_get_at.append(analytic.get_at)
    list_get_at.reverse()
  sort_options = {
    'id': 'video__video_number',
    'view': 'YouTubeView',
    'like': 'YouTubeLike',
    'comment': 'YouTubeComment'
  }
  sort_field = sort_options.get(request.GET.get('sort'), 'video__video_number')
  order = '' if request.GET.get('order')=='asc' else '-'
  analytics = Analytic.objects.filter(get_at=date.today()).order_by('{}{}'.format(order, sort_field))
  compare_date_str = request.GET.get('compare')
  if len(list_get_at) == 0:
    compare_date_date = date.today()
  elif len(list_get_at) == 1:
    compare_date_date = list_get_at[0]
  else:
    compare_date_date = list_get_at[1]
  if compare_date_str is not None:
    compare_date = tuple(map(int, re.match(r'([0-9]+)年([0-9]+)月([0-9]+)日', compare_date_str).groups()))
    print(compare_date)
    compare_date_date = date(compare_date[0], compare_date[1], compare_date[2])
    print(compare_date_date)
  context_analytics = []
  for analytic in analytics:
    try:
      comparedAnalytic = Analytic.objects.get(video=analytic.video, get_at=compare_date_date)
    except Analytic.DoesNotExist:
      comparedAnalytic = Analytic(
        video=analytic.video
      )
    context_analytics.append({
      'analytic': analytic,
      'totalView': analytic.totalStatistic()['view'],
      'totalLike': analytic.totalStatistic()['like'],
      'totalComment': analytic.totalStatistic()['comment'],
      'comparedStats': compareAnalytic(analytic, comparedAnalytic)
    })
  context = {
    'list_get_at': list_get_at,
    'analytics': context_analytics,
  }
  return render(request, "analytics/index.html", context)

def detail(request, video_number):
  try: 
    video = Video.objects.get(video_number=video_number)
  except Video.DoesNotExist:
    raise Http404("Video does not exist")
  analytics = Analytic.objects.filter(video=video).order_by('-get_at')
  context = {
    'video': video,
    'analytics': [{
      'analytic': analytic,
      'totalView': analytic.totalStatistic()['view'],
      'totalLike': analytic.totalStatistic()['like'],
      'totalComment': analytic.totalStatistic()['comment'],
    } for analytic in analytics]
  }
  return render(request, 'analytics/detail.html', context)

def fetch(request):
  if request.method == "POST":
    fetchAnalytics = FetchAnalytics()
    for fetchAnalytic in fetchAnalytics.items():
      fetchAnalyticJson = fetchAnalytic[1]
      video_id, get_at = fetchAnalyticJson['meta']['id'], fetchAnalyticJson['get_at']
      video, created = Video.objects.get_or_create(
        video_number=video_id,
        title=fetchAnalyticJson['meta']['title'],
        posted_at=fetchAnalyticJson['meta']['posted_at'],
        YouTube=fetchAnalyticJson['meta']['YouTube'],
        niconico=fetchAnalyticJson['meta']['niconico']
      )
      analytic, created = Analytic.objects.update_or_create(
        video=video,
        get_at=get_at,
        defaults={
          "YouTubeView": fetchAnalyticJson['stats']['view']['YouTube'],
          "YouTubeLike": fetchAnalyticJson['stats']['like']['YouTube'],
          "YouTubeComment": fetchAnalyticJson['stats']['comment']['YouTube'],
          "niconicoView": fetchAnalyticJson['stats']['view']['niconico'],
          "niconicoLike": fetchAnalyticJson['stats']['like']['niconico'],
          "niconicoComment": fetchAnalyticJson['stats']['comment']['niconico'],
          "niconicoMylist": fetchAnalyticJson['stats']['mylist']['niconico']
        },
        create_defaults={
          "YouTubeView": fetchAnalyticJson['stats']['view']['YouTube'],
          "YouTubeLike": fetchAnalyticJson['stats']['like']['YouTube'],
          "YouTubeComment": fetchAnalyticJson['stats']['comment']['YouTube'],
          "niconicoView": fetchAnalyticJson['stats']['view']['niconico'],
          "niconicoLike": fetchAnalyticJson['stats']['like']['niconico'],
          "niconicoComment": fetchAnalyticJson['stats']['comment']['niconico'],
          "niconicoMylist": fetchAnalyticJson['stats']['mylist']['niconico']
        }
      )
    return redirect('top')
  return render(request, 'analytics/fetch.html')