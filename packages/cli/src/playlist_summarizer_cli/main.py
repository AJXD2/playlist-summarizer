import os
import rich
import rich.progress
import rich.status
from rich.console import Console
from playlist_summarizer_core import get_playlist_videos, get_transcript, Summarizer
import inquirer
import dotenv
dotenv.load_dotenv()

console = Console()



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
    # Get configuration
    questions = [
        inquirer.Text("directory_path", message="Enter the directory path", default="transcripts/"),
        inquirer.Text("model", message="Enter the model to use", default="gemma3:4b"),
        inquirer.Text("output_dir", message="Enter the output directory", default="summaries/"),
    ]
    answers = inquirer.prompt(questions)
    model = answers["model"]
    output_dir = answers["output_dir"]
    directory_path = answers["directory_path"] or "transcripts/"
    
    if not os.path.exists(directory_path):
        console.print(f"[red]Error:[/red] Directory {directory_path} does not exist")
        return
    
    # Get playlists
    playlists = [p for p in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, p))]
    if len(playlists) == 0:
        console.print(f"[red]Error:[/red] No playlists found in {directory_path}")
        return
    
    questions = [
        inquirer.List("playlist", message="Select a playlist", choices=playlists, carousel=True),
    ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    playlist = answers["playlist"]
    
    playlist_path = os.path.join(directory_path, playlist)
    videos = [v for v in os.listdir(playlist_path) if v.endswith(".txt") and os.path.isfile(os.path.join(playlist_path, v))]
    
    if len(videos) == 0:
        console.print(f"[red]Error:[/red] No transcript files found in {playlist_path}")
        return
    
    # Ask which videos to summarize
    questions = [
        inquirer.Checkbox("selected_videos", message="Select videos to summarize (use space to select, enter to confirm)", choices=videos, default=videos),
    ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    selected_videos = answers["selected_videos"]
    
    if not selected_videos:
        console.print("[yellow]No videos selected. Exiting.[/yellow]")
        return
    
    # Initialize summarizer
    with rich.status.Status(f"[bold blue]Initializing summarizer with model '{model}'...[/bold blue]") as status:
        try:
            summarizer = Summarizer(model=model)
            status.update("[bold green]✓ Summarizer initialized[/bold green]")
        except Exception as e:
            console.print(f"[red]Error initializing summarizer:[/red] {e}")
            return
    
    # Create output directory
    output_playlist_dir = os.path.join(output_dir, playlist)
    os.makedirs(output_playlist_dir, exist_ok=True)
    
    # Process videos with progress tracking
    total_videos = len(selected_videos)
    successful = 0
    failed = 0
    
    with rich.progress.Progress(
        rich.progress.SpinnerColumn(),
        rich.progress.TextColumn("[progress.description]{task.description}"),
        rich.progress.BarColumn(),
        rich.progress.TextColumn("•"),
        rich.progress.TextColumn("[cyan]{task.completed}/{task.total}[/cyan]"),
        refresh_per_second=10
    ) as progress:
        main_task = progress.add_task(
            f"[bold cyan]Summarizing {total_videos} video{'s' if total_videos > 1 else ''}...[/bold cyan]",
            total=total_videos
        )
        
        for idx, video in enumerate(selected_videos, 1):
            video_path = os.path.join(playlist_path, video)
            output_path = os.path.join(output_playlist_dir, f"{video}.summary.md")
            
            # Skip if already exists
            if os.path.exists(output_path):
                progress.update(main_task, description=f"[yellow]Skipping {video} (already exists)[/yellow]")
                successful += 1
                progress.advance(main_task)
                continue
            
            progress.update(main_task, description=f"[bold cyan]Summarizing {video} ({idx}/{total_videos})...[/bold cyan]")
            
            try:
                summary = summarizer.summarize_file(video_path)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(summary)
                successful += 1
            except Exception as e:
                console.print(f"\n[red]✗ Failed to summarize {video}:[/red] {e}")
                failed += 1
            
            progress.advance(main_task)
    questions = [
        inquirer.Confirm("summarize_summaries", message="Do you want to summarize the summaries?"),
    ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    summarize_summaries = answers["summarize_summaries"]
    if not summarize_summaries:
        console.print("\n[bold green]Summary complete![/bold green]")
        console.print(f"  [green]✓ Successful:[/green] {successful}")
        if failed > 0:
            console.print(f"  [red]✗ Failed:[/red] {failed}")
        console.print(f"  [blue]Output directory:[/blue] {output_playlist_dir}")

    summary_files = [f for f in os.listdir(output_playlist_dir) if f.endswith(".summary.md")]
    summaries = [open(os.path.join(output_playlist_dir, f), "r", encoding="utf-8").read() for f in summary_files]
    summary = summarizer.summarize("\n".join(summaries))
    print(summary)
    with open(os.path.join(output_playlist_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write(summary)
    console.print(f"Summary saved to {os.path.join(output_playlist_dir, "summary.md")}")

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

