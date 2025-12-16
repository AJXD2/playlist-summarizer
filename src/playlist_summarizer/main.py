import os
from .fetcher import Video, get_playlist_videos, get_transcript
import rich
import inquirer

def fetch_playlist() -> None:
    questions = [
        inquirer.Text("playlist_url", message="Enter the playlist URL"),
        inquirer.Text("output_dir", message="Enter the output directory"),
    ]
    answers = inquirer.prompt(questions)
    playlist_url = answers["playlist_url"]
    output_dir = answers["output_dir"]

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

def main() -> None:
    questions = [
        inquirer.List("action", message="What do you want to do?", choices=["Fetch playlist", "Summarize playlist"]),
    ]
    answers = inquirer.prompt(questions)
    action = answers["action"]
    if action == "Fetch playlist":
        fetch_playlist()
    elif action == "Summarize playlist":
        print("Not implemented yet")
    else:
        # You never know
        print("Invalid action")

if __name__ == "__main__":
    main()