import isodate
from datetime import datetime
from googleapiclient.discovery import build
from django.conf import settings


class YouTubeAPI:
    """
    YouTube API class
    """
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.youtube = build(
            'youtube',
            'v3',
            developerKey=self.api_key
        )

    def search(self, q, max_results=10):
        """
        Search for videos on YouTube
        """
        search_results = self.youtube.search().list(
            q=q,
            part='snippet',
            type='video',
            maxResults=max_results
        ).execute()
        return search_results

    def _video(self, video_id):
        """
        Private method to get video details
        """
        video = self.youtube.videos().list(
            part='snippet,contentDetails',
            id=video_id
        ).execute()
        return video

    def video_duration(self, video_id):
        """
        Get video duration
        """
        video = self._video(video_id)
        duration = video['items'][0]['contentDetails']['duration']
        formatted_duration = str(isodate.parse_duration(duration)).split('.')[0]
        return formatted_duration

    def video_posted_date(self, video_id):
        """
        Get video posted date
        """
        video = self._video(video_id)
        date = video['items'][0]['snippet']['publishedAt']
        formatted_date = datetime.strptime(
            date,
            '%Y-%m-%dT%H:%M:%SZ'
        ).strftime('%b %d, %Y')
        return formatted_date

    def video_channel_name(self, video_id):
        """
        Get video channel name
        """
        video = self._video(video_id)
        channel_name = video['items'][0]['snippet']['channelTitle']
        return channel_name
