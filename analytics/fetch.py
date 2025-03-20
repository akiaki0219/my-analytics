import datetime, json, os, requests
from googleapiclient.discovery import build
from supabase import create_client, Client

def fetchYouTubeAPI(videoId: str|None):
  if videoId is None:
    statistics = {
      "viewCount": 0,
      "likeCount": 0,
      "favoriteCount": 0,
      "commentCount": 0
    }
  else:
    response = build('youtube', 'v3', developerKey=os.environ.get("YOUTUBE_KEY")).videos().list(part='statistics', id=videoId).execute()
    statistics = response["items"][0]["statistics"]
  return statistics
def fetchNicoNicoAPI(videoId: str|None):
  if videoId is None:
    data = {
      "viewCounter": 0,
      "likeCounter": 0,
      "mylistCounter": 0,
      "commentCounter": 0
    }
  else:
    response = requests.get('https://snapshot.search.nicovideo.jp/api/v2/snapshot/video/contents/search?q=&fields=viewCounter,mylistCounter,likeCounter,commentCounter&filters[contentId][0]={}&_sort=-viewCounter&_context=analytics'.format(videoId))
    response_json = json.loads(response.content.decode())
    data = response_json["data"][0]
  return data
def fetchSupabaseAPI(supabaseClient: Client):
  response = supabaseClient.table('video').select('id, YouTube, niconico').eq('public', True).execute()
  data = response.data
  return data

def FetchAnalytics():
  supabaseClient: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
  videoList = fetchSupabaseAPI(supabaseClient)
  analytics = {}
  id = 0
  for video in videoList:
    YouTubeData = fetchYouTubeAPI(video['YouTube'])
    niconicoData = fetchNicoNicoAPI(video['niconico'])
    videoId = video['id']
    YouTubeView, niconicoView = YouTubeData['viewCount'], niconicoData['viewCounter']
    YouTubeLike, niconicoLike = YouTubeData['likeCount'], niconicoData['likeCounter']
    YouTubeComment, niconicoComment = YouTubeData['commentCount'], niconicoData['commentCounter']
    niconicoMylist = niconicoData['mylistCounter']
    analytic = {
      "view": {
        "YouTube": YouTubeView,
        "niconico": niconicoView
      },
      "like": {
        "YouTube": YouTubeLike,
        "niconico": niconicoLike
      },
      "comment": {
        "YouTube": YouTubeComment,
        "niconico": niconicoComment
      },
      "mylist": {
        "niconico": niconicoMylist
      }
    }
    analytics[id] = {
      "videoId": videoId,
      "get_at": datetime.date.today(),
      "analytic": analytic
    }
    id += 1
  return analytics

"""
fetchAnalytics = FetchAnalytics()
fetchAnalytic = fetchAnalytics[1]
analytic = {
  'videoId': fetchAnalytic['videoId'],
  'get_at': fetchAnalytic['get_at'],
  'YouTubeView': fetchAnalytic['analytic']['view']['YouTube'],
  'YouTubeLike': fetchAnalytic['analytic']['like']['YouTube'],
  'YouTubeComment': fetchAnalytic['analytic']['comment']['YouTube'],
  'niconicoView': fetchAnalytic['analytic']['view']['niconico'],
  'niconicoLike': fetchAnalytic['analytic']['like']['niconico'],
  'niconicoComment': fetchAnalytic['analytic']['comment']['niconico'],
  'niconicoMylist': fetchAnalytic['analytic']['mylist']['niconico']
}
print(analytic)
"""