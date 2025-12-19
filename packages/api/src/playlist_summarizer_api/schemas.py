from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="ok", description="API health status")
    details: str = Field(default="", description="Detailed health information")
