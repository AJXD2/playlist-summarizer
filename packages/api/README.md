# Playlist Summarizer API

FastAPI REST API for fetching YouTube playlist transcripts and generating AI-powered summaries.

## Installation

This package is part of the playlist-summarizer monorepo. Install dependencies using `uv`:

```bash
uv sync
```

## Configuration

The API uses environment variables for configuration. Create a `.env` file in the project root:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_API_KEY=your_api_key_here
DEFAULT_MODEL=gemma3:4b
```

### Settings

- `OLLAMA_HOST` (optional): Ollama server host URL. Defaults to `http://localhost:11434` if not set.
- `OLLAMA_API_KEY` (optional): API key for Ollama cloud models (required for models ending with `-cloud`).
- `DEFAULT_MODEL` (optional): Default Ollama model to use for summarization. Defaults to `gemma3:4b`.

## Running the API

### Using the script entry point

```bash
uv run playlist-summarizer-api
```

### Using uvicorn directly

```bash
uv run uvicorn playlist_summarizer_api.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, interactive API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Health Check

- **GET** `/health` - Returns API health status

## Development

The API uses:

- FastAPI for the web framework
- Pydantic for request/response validation
- Uvicorn as the ASGI server
- `playlist-summarizer-core` for core functionality
