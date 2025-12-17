# Playlist Summarizer

A Python CLI tool that fetches YouTube playlist transcripts and generates AI-powered summaries using local or cloud-based LLM models via Ollama.

## Features

- 📥 **Fetch Playlists**: Download transcripts from YouTube playlists
- 🤖 **AI Summarization**: Generate summaries using Ollama models (local or cloud)
- 📝 **Markdown Output**: Clean, structured summaries in Markdown format
- 🎯 **Selective Processing**: Choose which videos to summarize
- 📊 **Progress Tracking**: Real-time progress bars and status updates
- 🔒 **Secure Prompts**: Hardened system prompts resistant to injection attacks
- 🎨 **Rich CLI**: Beautiful terminal interface with colors and formatting

## Requirements

- Python 3.14+
- [Ollama](https://ollama.com/) installed and running (for local models)
- Or Ollama Cloud API key (for cloud models)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ajxd2/playlist-summarizer.git
cd playlist-summarizer
```

2. Install dependencies using `uv`:
```bash
uv sync
```

3. (Optional) Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add:
# OLLAMA_HOST=http://localhost:11434  # Optional, defaults to localhost
# OLLAMA_API_KEY=your_api_key_here     # Required for cloud models
```

## Usage

Run the application:
```bash
uv run playlist-summarizer
```

Or activate the virtual environment and run:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
playlist-summarizer
```

### Fetch Playlist Transcripts

1. Select "Fetch playlist" from the main menu
2. Enter the YouTube playlist URL
3. Specify the output directory (defaults to `transcripts/{playlist_id}/`)
4. Transcripts will be saved as `.txt` files

### Summarize Playlists

1. Select "Summarize playlist" from the main menu
2. Enter the directory path containing transcripts (defaults to `transcripts/`)
3. Choose the Ollama model to use (e.g., `gemma3:4b`, `llama3.1:8b`, `qwen2.5:7b`)
4. Specify the output directory for summaries (defaults to `summaries/`)
5. Select a playlist folder
6. Choose which videos to summarize (use space to select/deselect)
7. Optionally create a master summary of all video summaries


## Project Structure

```
playlist-summarizer/
├── src/
│   └── playlist_summarizer/
│       ├── __init__.py
│       ├── __main__.py
│       ├── main.py          # CLI entry point
│       ├── fetcher.py        # YouTube transcript fetching
│       └── summarizer.py    # AI summarization logic
├── transcripts/             # Downloaded transcripts (gitignored)
├── summaries/              # Generated summaries (gitignored)
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
└── README.md
```

## Configuration

### Environment Variables

- `OLLAMA_HOST` - Ollama server URL (default: `http://localhost:11434`)
- `OLLAMA_API_KEY` - API key for Ollama Cloud (required for cloud models)

### Default Directories

- Transcripts: `transcripts/`
- Summaries: `summaries/`

## Development

### Setup Development Environment

```bash
uv sync
```

### Run from Source

```bash
uv run python -m playlist_summarizer
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Anthony Kovach - [aj@ajxd2.dev](mailto:aj@ajxd2.dev)

