import uvicorn
from fastapi import FastAPI

from .schemas import HealthResponse

app = FastAPI(
    title="Playlist Summarizer API",
    description="REST API for fetching YouTube playlist transcripts and generating AI-powered summaries",
    version="0.1.0",
    docs_url="/docs",
)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


def main() -> None:
    uvicorn.run(
        "playlist_summarizer_api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
