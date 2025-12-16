import os
from .fetcher import Video, get_playlist_videos, get_transcript


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