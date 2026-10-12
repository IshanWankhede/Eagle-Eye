from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter(prefix="/api", tags=["health"])
APP_VERSION = "0.1.0"


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    # Scaffold only: the detector is not implemented yet, so model_loaded is always False.
    return HealthResponse(
        status="ok",
        version=APP_VERSION,
        model_loaded=False,
        model_file_found=settings.model_file_exists,
    )
