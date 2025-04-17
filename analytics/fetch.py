import datetime
import dotenv
import json
import os
import requests
from googleapiclient.discovery import build
from supabase import create_client, Client

dotenv.load_dotenv()
DEVELOPER_KEY = os.getenv("YOUTUBE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_WEB_URL")
SUPABASE_KEY = os.getenv("SUPABASE_WEB_KEY")


def fetchYouTubeAPI(videoId: str | None):
    if videoId is None:
        statistics = {
            "viewCount": 0,
            "likeCount": 0,
            "favoriteCount": 0,
            "commentCount": 0
        }
    else:
        response = build('youtube', 'v3', developerKey=DEVELOPER_KEY).videos().list(part='statistics', id=videoId).execute()
        statistics = response["items"][0]["statistics"]
    return statistics


def fetchNicoNicoAPI(videoId: str | None):
    if videoId is None:
        data = {
            "viewCounter": 0,
            "likeCounter": 0,
            "mylistCounter": 0,
            "commentCounter": 0
        }
    else:
        response = requests.get((
            'https://snapshot.search.nicovideo.jp/'
            'api/v2/snapshot/video/contents/search?'
            'q=&fields=viewCounter,mylistCounter,likeCounter,commentCounter&'
            'filters[contentId][0]={}&_sort=-viewCounter&_context=analytics'
            ).format(videoId))
        response_json = json.loads(response.content.decode())
        data = response_json["data"][0]
    return data


def fetchSupabaseAPI(supabaseClient: Client):
    response = supabaseClient.table('video').select('id, title, posted_at, YouTube, niconico').eq('public', True).execute()
    data = response.data
    return data


def FetchAnalytics():
    supabaseClient: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    videoList = fetchSupabaseAPI(supabaseClient)
    analytics = {}
    id = 0
    for video in videoList:
        meta = {
            "id": video['id'],
            "title": video['title'],
            "posted_at": video['posted_at'],
            "YouTube": video['YouTube'],
            "niconico": video['niconico']
        }
        YouTubeData = fetchYouTubeAPI(meta['YouTube'])
        niconicoData = fetchNicoNicoAPI(meta['niconico'])
        stats = {
            "view": {
                "YouTube": int(YouTubeData['viewCount']),
                "niconico": int(niconicoData['viewCounter'])
            },
            "like": {
                "YouTube": int(YouTubeData['likeCount']),
                "niconico": int(niconicoData['likeCounter'])
            },
            "comment": {
                "YouTube": int(YouTubeData['commentCount']),
                "niconico": int(niconicoData['commentCounter'])
            },
            "mylist": {
                "niconico": int(niconicoData['mylistCounter'])
            }
        }
        analytics[id] = {
            "get_at": datetime.date.today(),
            "meta": meta,
            "stats": stats
        }
        id += 1
    return analytics
