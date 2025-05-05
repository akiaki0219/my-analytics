import re
from analytics.fetch import FetchAnalytics
from analytics.models import Analytic, Video, compareAnalytic
from datetime import date
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie


def index(request):
    status = 'Not fetched'
    query_strings = {
        'sort': request.GET.get('sort'),
        'sort_option': request.GET.get('sort-option'),
        'order': request.GET.get('order'),
        'compare': request.GET.get('compare'),
        'non_zero': request.GET.get('non-zero'),
        'non_zero_target': request.GET.get('non-zero-target'),
        'non_zero_option': request.GET.get('non-zero-option')
    }
    if query_strings['sort'] not in [None, 'id', 'view', 'like', 'comment', 'mylist']:
        query_strings['sort'] = 'id'
    if query_strings['sort_option'] not in [None, 'total', 'youtube', 'niconico']:
        query_strings['sort_option'] = 'total'
    if query_strings['order'] not in [None, 'asc', 'desc']:
        query_strings['order'] = 'desc'
    if query_strings['non_zero_target'] not in [None, 'all', 'view', 'like', 'comment', 'mylist']:
        query_strings['non_zero_target'] = 'all'
    if query_strings['non_zero_option'] not in [None, 'total', 'youtube', 'niconico']:
        query_strings['non_zero_option'] = 'total'
    sort, sort_option = query_strings['sort'], query_strings['sort_option']
    order, compare_date_str = query_strings['order'], query_strings['compare']
    non_zero, non_zero_target = query_strings['non_zero'], query_strings['non_zero_target']
    non_zero_option = query_strings['non_zero_option']
    today = date.today()
    analytic_first = Analytic.objects.filter(get_at=today).order_by('video__video_number').first()
    list_get_at = []
    if analytic_first:
        status = 'Have fetched'
        for analytic in Analytic.objects.filter(video=Video.objects.get(video_number=analytic_first.video.video_number)):
            list_get_at.append(analytic.get_at)
        list_get_at.sort(reverse=True)
        if len(list_get_at) >= 2:
            list_get_at = list_get_at[1:]
    if compare_date_str is not None:
        compare_date = tuple(map(int, re.match(r'([0-9]+)-([0-9]+)-([0-9]+)', compare_date_str).groups()))
        compare_date_date = date(compare_date[0], compare_date[1], compare_date[2])
    else:
        if len(list_get_at) == 0:
            compare_date_date = today
        else:
            compare_date_date = list_get_at[0]
    list_get_at = list(map(str, list_get_at))
    sort_options = {
        'total': {
            'view': 'totalView',
            'like': 'totalLike',
            'comment': 'totalComment',
            'mylist': 'totalMylist'
        },
        'youtube': {
            'view': 'YouTubeView',
            'like': 'YouTubeLike',
            'comment': 'YouTubeComment',
            'mylist': 'niconicoMylist'
        },
        'niconico': {
            'view': 'niconicoView',
            'like': 'niconicoLike',
            'comment': 'niconicoComment',
            'mylist': 'niconicoMylist'
        }
    }
    if sort_option in ['youtube', 'niconico'] and sort is not None:
        if sort == "id":
            analytics = Analytic.objects.filter(get_at=date.today())\
                .order_by("{}video__video_number".format("" if order == "asc" else "-"))
        else:
            analytics = Analytic.objects.filter(get_at=date.today())\
                .order_by("{}{}".format("" if order == "asc" else "-", sort_options[sort_option][sort]))
    else:
        analytics = Analytic.objects.filter(get_at=date.today())\
            .order_by("{}video__video_number".format("" if order == "asc" else "-"))
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
            'totalMylist': analytic.niconicoMylist,
            'comparedStats': compareAnalytic(analytic, comparedAnalytic)
        })
    if sort is not None and sort != 'id' and sort_option == 'total':
        analytics = sorted(context_analytics,
                           key=lambda analytic: analytic[sort_options['total'][sort]], reverse=(order != 'asc'))
    else:
        analytics = context_analytics
    if non_zero == 'on':
        context_analytics = []
        if non_zero_target == 'all' or non_zero_target is None:
            for analytic in analytics:
                compared_stats = analytic['comparedStats']
                if non_zero_option == 'youtube':
                    target_compared_stats = [
                        compared_stats['view']['YouTube'],
                        compared_stats['like']['YouTube'],
                        compared_stats['comment']['YouTube']
                    ]
                elif non_zero_option == 'niconico':
                    target_compared_stats = [
                        compared_stats['view']['niconico'],
                        compared_stats['like']['niconico'],
                        compared_stats['comment']['niconico'],
                        compared_stats['mylist']['niconico']
                    ]
                else:
                    target_compared_stats = [
                        compared_stats['view']['total'],
                        compared_stats['like']['total'],
                        compared_stats['comment']['total'],
                        compared_stats['mylist']['niconico']
                    ]
                if any([i != 0 for i in target_compared_stats]):
                    context_analytics.append(analytic)
        else:
            if non_zero_option is None:
                non_zero_option = 'total'
            elif non_zero_option == 'youtube':
                non_zero_option = 'YouTube'
            if non_zero_target == 'mylist':
                non_zero_option = 'niconico'
            for analytic in analytics:
                compared_stat = analytic['comparedStats'][non_zero_target][non_zero_option]
                if compared_stat != 0:
                    context_analytics.append(analytic)
        analytics = context_analytics
        if len(analytics) == 0:
            status = 'No data'
    context = {
        'status': status,
        'query_strings': query_strings,
        'list_get_at': list_get_at,
        'analytics': analytics,
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


@ensure_csrf_cookie
def fetch(request):
    if request.method == "POST":
        fetch_analytics = FetchAnalytics()
        for i in fetch_analytics:
            fetch_analytic = fetch_analytics[i]
            video_id, get_at = fetch_analytic['meta']['id'], fetch_analytic['get_at']
            video, created = Video.objects.get_or_create(
                video_number=video_id,
                title=fetch_analytic['meta']['title'],
                posted_at=fetch_analytic['meta']['posted_at'],
                YouTube=fetch_analytic['meta']['YouTube'],
                niconico=fetch_analytic['meta']['niconico']
            )
            analytic, created = Analytic.objects.update_or_create(
                video=video,
                get_at=get_at,
                defaults={
                    "YouTubeView": fetch_analytic['stats']['view']['YouTube'],
                    "YouTubeLike": fetch_analytic['stats']['like']['YouTube'],
                    "YouTubeComment": fetch_analytic['stats']['comment']['YouTube'],
                    "niconicoView": fetch_analytic['stats']['view']['niconico'],
                    "niconicoLike": fetch_analytic['stats']['like']['niconico'],
                    "niconicoComment": fetch_analytic['stats']['comment']['niconico'],
                    "niconicoMylist": fetch_analytic['stats']['mylist']['niconico']
                },
                create_defaults={
                    "YouTubeView": fetch_analytic['stats']['view']['YouTube'],
                    "YouTubeLike": fetch_analytic['stats']['like']['YouTube'],
                    "YouTubeComment": fetch_analytic['stats']['comment']['YouTube'],
                    "niconicoView": fetch_analytic['stats']['view']['niconico'],
                    "niconicoLike": fetch_analytic['stats']['like']['niconico'],
                    "niconicoComment": fetch_analytic['stats']['comment']['niconico'],
                    "niconicoMylist": fetch_analytic['stats']['mylist']['niconico']
                }
            )
        for i in fetch_analytics:
            analytics = Analytic.objects.filter(video=Video.objects.get(video_number=fetch_analytics[i]['meta']['id']), get_at=date.today())
            if len(analytics) >= 2:
                analytics[1:].delete()
        return redirect('top')
    return render(request, 'analytics/fetch.html')
