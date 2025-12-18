from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL


class Video:
    def __init__(self, url: str, title: str):
        self.url = url
        self.title = title


def get_playlist_videos(playlist_url: str) -> list[Video]:
    with YoutubeDL() as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)

        videos = [Video(entry["id"], entry["title"]) for entry in info_dict["entries"]]
        return videos


def get_transcript(video: Video) -> str:
    transcript = YouTubeTranscriptApi().fetch(video.url)

    return "\n".join(
        [snippet.text for snippet in sorted(transcript.snippets, key=lambda x: x.start)]
    )
