from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
import os

class Video:
    def __init__(self, url: str, title: str):
        self.url = url
        self.title = title

def get_playlist_videos(playlist_url: str) -> list[Video]:
    with YoutubeDL() as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
       
        videos = [Video(entry['id'], entry['title']) for entry in info_dict['entries']]
        return videos

def get_transcript(video: Video) -> str:
    transcript = YouTubeTranscriptApi().fetch(video.url)
    
    return "\n".join([snippet.text for snippet in sorted(transcript.snippets, key=lambda x: x.start)])

def main() -> None:
    playlist_url = input("Enter the playlist URL: ")
    output_dir = input("Enter the output directory: ")

    playlist_id = playlist_url.split("list=")[1]

    if output_dir == "":
        output_dir = f"transcripts/{playlist_id}/"
    os.makedirs(output_dir, exist_ok=True)
    videos = get_playlist_videos(playlist_url)
    for video in videos:
        transcript = get_transcript(video)
        with open(os.path.join(output_dir, f"{video.title} ({video.url}).txt"), "w") as f:
            f.write(transcript)
        print(f"Transcript for {video.title} saved to {os.path.join(output_dir, f"{video.title} ({video.url}).txt")}")

if __name__ == "__main__":
    main()