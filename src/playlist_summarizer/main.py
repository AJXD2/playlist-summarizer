import os
from .fetcher import get_playlist_videos, get_transcript
import inquirer
from .summarizer import Summarizer
import dotenv
dotenv.load_dotenv()



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

def summarize_playlist() -> None:
    questions = [
        inquirer.Text("directory_path", message="Enter the directory path", default="transcripts/"),
        inquirer.Text("model", message="Enter the model to use", default="gemma3:4b"),
    ]
    answers = inquirer.prompt(questions)
    summarizer = Summarizer(model=answers["model"])
    directory_path = answers["directory_path"]
    if directory_path == "":
        directory_path = "transcripts/"
    
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist")
        return
    
    # Get files (playlists)
    playlists = os.listdir(directory_path)
    if len(playlists) == 0:
        print(f"No files found in {directory_path}")
        return
    
    # Display files to user
    questions = [
        inquirer.List("playlist", message="Select a playlist", choices=playlists, carousel=True),
    ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    playlist = answers["playlist"]

    if not os.path.exists(os.path.join(directory_path, playlist)):
        print(f"Playlist {playlist} does not exist")
        return
    
    # Get video transcripts from directory
    videos = os.listdir(os.path.join(directory_path, playlist))
    if len(videos) == 0:
        print(f"No videos found in {os.path.join(directory_path, playlist)}")
        return
    
    # get video to summarize
    questions = [
        inquirer.List("video", message="Select a video", choices=videos, carousel=True),
    ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    video = answers["video"]
    
    # Summarize video
    summary = summarizer.summarize_file(os.path.join(directory_path, playlist, video))
    print(summary)
def main() -> None:
    try:
        questions = [
            inquirer.List("action", message="What do you want to do?", choices=["Fetch playlist", "Summarize playlist"], carousel=True),
        ]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        action = answers["action"]
        if action == "Fetch playlist":
            fetch_playlist()
        elif action == "Summarize playlist":
            summarize_playlist()
        else:
            # You never know
            print("Invalid action")
    except KeyboardInterrupt:
        print("exiting...")
        exit(0)
    
if __name__ == "__main__":
    main()