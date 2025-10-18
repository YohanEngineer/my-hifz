"""
API routes for memorization planning and PDF generation.
Contains endpoints for generating schedules and downloading PDFs.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.models import PlanningSettings
from app.services.planning_service import planning_service
from app.services.pdf_service import pdf_service
from app.config import logger

router = APIRouter(
    prefix="/api/v1/plan",
    tags=["planning"]
)


@router.post("/generate")
async def generate_plan(settings: PlanningSettings):
    """
    Generate a memorization schedule and return it as a downloadable PDF.

    This endpoint executes the full planning algorithm:
    1. Determines the direction based on order (Ascending/Descending)
    2. Iterates through pages, grouping them by pages_per_period
    3. For each period, creates an object with period_label, page_range, surahs, and juzs
    4. Generates a PDF with the schedule formatted as a table with Arabic Surah names
    5. Returns the PDF as a FileResponse for immediate download

    Args:
        settings: Planning settings (pages_per_period, period_type, start_page, order)

    Returns:
        StreamingResponse with PDF file

    Raises:
        HTTPException: If schedule generation or PDF creation fails
    """
    try:
        logger.info(f"Received plan generation request: {settings.model_dump()}")

        # Generate the schedule
        schedule = planning_service.generate_schedule(settings)

        if not schedule:
            raise HTTPException(
                status_code=400,
                detail="Generated schedule is empty. Please check your settings."
            )

        # Generate PDF
        pdf_buffer = pdf_service.generate_schedule_pdf(settings, schedule)

        # Return PDF as streaming response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=Hifz_Planner_Schedule.pdf"
            }
        )

    except RuntimeError as e:
        logger.error(f"Runtime error during plan generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during plan generation: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate plan: {str(e)}"
        )
