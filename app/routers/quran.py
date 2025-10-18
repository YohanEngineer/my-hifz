"""
API routes for Quran page data.
Contains all endpoints for retrieving Quran information.
"""

from typing import List
from fastapi import APIRouter, HTTPException

from app.models import PageData
from app.services.quran_service import quran_service
from app.config import logger, settings

router = APIRouter(
    prefix="/api/quran",
    tags=["quran"]
)


@router.get("/pages", response_model=List[PageData])
async def get_all_pages():
    """
    Retrieve all 604 Quran pages.

    Returns:
        List of all page data

    Raises:
        HTTPException: If data is not loaded
    """
    try:
        pages = quran_service.get_all_pages()
        logger.debug(f"Returning all {len(pages)} pages")
        return pages
    except RuntimeError as e:
        logger.error(f"Failed to get all pages: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pages/{page_number}", response_model=PageData)
async def get_page(page_number: int):
    """
    Retrieve a specific Quran page by number.

    Args:
        page_number: Page number (1-604)

    Returns:
        Page data for the requested page

    Raises:
        HTTPException: If page number is invalid or not found
    """
    if page_number < 1 or page_number > settings.TOTAL_PAGES:
        logger.warning(f"Invalid page number requested: {page_number}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid page number. Must be between 1 and {settings.TOTAL_PAGES}, got {page_number}"
        )

    try:
        page = quran_service.get_page(page_number)
        if page is None:
            raise HTTPException(
                status_code=404,
                detail=f"Page {page_number} not found"
            )

        logger.debug(f"Returning page {page_number}")
        return page

    except RuntimeError as e:
        logger.error(f"Failed to get page {page_number}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pages/surah/{surah_number}", response_model=List[PageData])
async def get_pages_by_surah(surah_number: int):
    """
    Retrieve all pages for a specific Surah.

    Args:
        surah_number: Surah number (1-114)

    Returns:
        List of pages containing ayahs from the specified Surah

    Raises:
        HTTPException: If surah number is invalid or no pages found
    """
    if surah_number < 1 or surah_number > settings.TOTAL_SURAHS:
        logger.warning(f"Invalid Surah number requested: {surah_number}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Surah number. Must be between 1 and {settings.TOTAL_SURAHS}, got {surah_number}"
        )

    try:
        pages = quran_service.get_pages_by_surah(surah_number)
        if not pages:
            raise HTTPException(
                status_code=404,
                detail=f"No pages found for Surah {surah_number}"
            )

        logger.debug(f"Returning {len(pages)} pages for Surah {surah_number}")
        return pages

    except RuntimeError as e:
        logger.error(f"Failed to get pages for Surah {surah_number}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pages/juz/{juz_number}", response_model=List[PageData])
async def get_pages_by_juz(juz_number: int):
    """
    Retrieve all pages for a specific Juz.

    Args:
        juz_number: Juz number (1-30)

    Returns:
        List of pages in the specified Juz

    Raises:
        HTTPException: If juz number is invalid or no pages found
    """
    if juz_number < 1 or juz_number > settings.TOTAL_JUZ:
        logger.warning(f"Invalid Juz number requested: {juz_number}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Juz number. Must be between 1 and {settings.TOTAL_JUZ}, got {juz_number}"
        )

    try:
        pages = quran_service.get_pages_by_juz(juz_number)
        if not pages:
            raise HTTPException(
                status_code=404,
                detail=f"No pages found for Juz {juz_number}"
            )

        logger.debug(f"Returning {len(pages)} pages for Juz {juz_number}")
        return pages

    except RuntimeError as e:
        logger.error(f"Failed to get pages for Juz {juz_number}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
