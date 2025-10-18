"""
My Hifz Planner - FastAPI Backend
Main application entry point for serving Quran page data and scheduling logic.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings, logger
from app.services.quran_service import quran_service
from app.routers import quran, planning


# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Include routers
app.include_router(quran.router)
app.include_router(planning.router)


@app.on_event("startup")
async def startup_event():
    """Load data when the application starts."""
    logger.info("Starting My Hifz Planner API")
    try:
        quran_service.load_data()
        logger.info(f"Application startup complete - {quran_service.page_count} pages loaded")
    except Exception as e:
        logger.error(f"Failed to load Quran data during startup: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup when the application shuts down."""
    logger.info("Shutting down My Hifz Planner API")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    logger.debug("Root endpoint accessed")
    return {
        "message": settings.API_TITLE,
        "version": settings.API_VERSION,
        "endpoints": {
            "GET /api/v1/quran/pages": "Get all Quran pages",
            "GET /api/v1/quran/pages/{page_number}": f"Get a specific page (1-{settings.TOTAL_PAGES})",
            "GET /api/v1/quran/pages/surah/{surah_number}": f"Get pages by Surah (1-{settings.TOTAL_SURAHS})",
            "GET /api/v1/quran/pages/juz/{juz_number}": f"Get pages by Juz (1-{settings.TOTAL_JUZ})",
            "POST /api/v1/plan/generate": "Generate memorization schedule PDF",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    is_healthy = quran_service.is_loaded
    status_code = 200 if is_healthy else 503

    response = {
        "status": "healthy" if is_healthy else "unhealthy",
        "pages_loaded": quran_service.page_count
    }

    logger.debug(f"Health check: {response}")
    return response
