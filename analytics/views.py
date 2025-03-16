from analytics.models import Analytic
from datetime import date
from django.http import Http404
from django.shortcuts import render

def index(request):
  if request.method == "POST":
    analytic = Analytic(
      videoId=request.POST['videoId'],
      videoTitle=request.POST['videoTitle'],
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
  if request.GET.get('order') == 'view':
    analytics = Analytic.objects.order_by('-YouTubeView')
  elif request.GET.get('order') == 'like':
    analytics = Analytic.objects.order_by('-YouTubeLike')
  elif request.GET.get('order') == 'comment':
    analytics = Analytic.objects.order_by('-YouTubeComment')
  else:
    analytics = Analytic.objects.order_by('-videoId')
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