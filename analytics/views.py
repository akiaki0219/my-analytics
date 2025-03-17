from analytics.models import Analytic
from datetime import date
from django.http import Http404
from django.shortcuts import render

def index(request):
  if request.method == "POST":
    analytic = Analytic(
      videoId=request.POST['videoId'],
      get_at=date.today(),
      YouTubeView=request.POST['YouTubeView'],
      YouTubeLike=request.POST['YouTubeLike'],
      YouTubeComment=request.POST['YouTubeComment'],
      niconicoView=request.POST['niconicoView'],
      niconicoLike=request.POST['niconicoLike'],
      niconicoComment=request.POST['niconicoComment'],
      niconicoMylist=request.POST['niconicoMylist']
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