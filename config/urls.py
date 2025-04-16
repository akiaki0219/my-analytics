from django.contrib import admin
from django.urls import path
from analytics import views as analytics_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', analytics_views.index, name='index'),
    path('top/', analytics_views.index, name='top'),
    path('video/<int:video_number>/', analytics_views.detail, name='detail'),
    path('fetch/', analytics_views.fetch, name='fetch'),
]
