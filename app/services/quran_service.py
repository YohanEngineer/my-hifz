"""
Service layer for Quran data management.
Handles loading and accessing Quran page data.
"""

import json
from typing import List, Optional
from pathlib import Path

from app.models import PageData
from app.config import logger, settings


class QuranService:
    """Service for managing Quran page data."""

    def __init__(self):
        """Initialize the Quran service."""
        self._pages: List[PageData] = []

    def load_data(self, json_path: Optional[Path] = None) -> None:
        """
        Load Quran data from JSON file.

        Args:
            json_path: Path to the JSON file (defaults to settings.QURAN_JSON_PATH)

        Raises:
            FileNotFoundError: If the JSON file doesn't exist
            ValueError: If the data cannot be parsed
        """
        path = json_path or settings.QURAN_JSON_PATH

        if not path.exists():
            logger.error(f"Quran data file not found: {path}")
            raise FileNotFoundError(
                f"quran.json not found at {path}. "
                "Please run generate_quran_data.py first."
            )

        logger.info(f"Loading Quran data from {path}")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)

            self._pages = [PageData(**page) for page in raw_data]
            logger.info(f"Successfully loaded {len(self._pages)} pages")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON file: {e}")
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            logger.error(f"Failed to load Quran data: {e}")
            raise

    def get_all_pages(self) -> List[PageData]:
        """
        Get all Quran pages.

        Returns:
            List of all page data

        Raises:
            RuntimeError: If data hasn't been loaded
        """
        if not self._pages:
            logger.error("Attempted to access pages before loading data")
            raise RuntimeError("Quran data not loaded")

        return self._pages

    def get_page(self, page_number: int) -> Optional[PageData]:
        """
        Get a specific Quran page by number.

        Args:
            page_number: Page number (1-604)

        Returns:
            Page data if found, None otherwise

        Raises:
            RuntimeError: If data hasn't been loaded
        """
        if not self._pages:
            logger.error("Attempted to access page before loading data")
            raise RuntimeError("Quran data not loaded")

        if page_number < 1 or page_number > settings.TOTAL_PAGES:
            logger.warning(f"Invalid page number requested: {page_number}")
            return None

        # Pages are 1-indexed, list is 0-indexed
        page_index = page_number - 1

        if page_index >= len(self._pages):
            logger.warning(f"Page {page_number} not found in loaded data")
            return None

        return self._pages[page_index]

    def get_pages_by_surah(self, surah_number: int) -> List[PageData]:
        """
        Get all pages containing ayahs from a specific Surah.

        Args:
            surah_number: Surah number (1-114)

        Returns:
            List of pages containing ayahs from the specified Surah

        Raises:
            RuntimeError: If data hasn't been loaded
        """
        if not self._pages:
            logger.error("Attempted to access pages before loading data")
            raise RuntimeError("Quran data not loaded")

        if surah_number < 1 or surah_number > settings.TOTAL_SURAHS:
            logger.warning(f"Invalid Surah number requested: {surah_number}")
            return []

        matching_pages = [
            page for page in self._pages
            if any(ayah.surah.number == surah_number for ayah in page.ayahs)
        ]

        logger.debug(f"Found {len(matching_pages)} pages for Surah {surah_number}")
        return matching_pages

    def get_pages_by_juz(self, juz_number: int) -> List[PageData]:
        """
        Get all pages in a specific Juz.

        Args:
            juz_number: Juz number (1-30)

        Returns:
            List of pages in the specified Juz

        Raises:
            RuntimeError: If data hasn't been loaded
        """
        if not self._pages:
            logger.error("Attempted to access pages before loading data")
            raise RuntimeError("Quran data not loaded")

        if juz_number < 1 or juz_number > settings.TOTAL_JUZ:
            logger.warning(f"Invalid Juz number requested: {juz_number}")
            return []

        matching_pages = [
            page for page in self._pages
            if any(ayah.juz == juz_number for ayah in page.ayahs)
        ]

        logger.debug(f"Found {len(matching_pages)} pages for Juz {juz_number}")
        return matching_pages

    @property
    def is_loaded(self) -> bool:
        """Check if data has been loaded."""
        return len(self._pages) > 0

    @property
    def page_count(self) -> int:
        """Get the number of loaded pages."""
        return len(self._pages)


# Global service instance
quran_service = QuranService()
