from analytics.models import Analytic
from datetime import date
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
  analytics = Analytic.objects.all()
  context = {
    'analytics': analytics
  }
  return render(request, "analytics/index.html", context)