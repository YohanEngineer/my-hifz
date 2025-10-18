"""
Service layer for memorization planning logic.
Handles schedule generation with ascending/descending order support.
"""

from typing import List, Dict
from app.models import PlanningSettings, PeriodSchedule, PageData
from app.services.quran_service import quran_service
from app.config import logger


class PlanningService:
    """Service for generating memorization schedules."""

    def generate_schedule(self, settings: PlanningSettings) -> List[Dict]:
        """
        Generate a memorization schedule based on user settings.

        Args:
            settings: Planning settings including pages_per_period, period_type, start_page, and order

        Returns:
            List of period schedules with page ranges, surahs, and juz information

        Raises:
            RuntimeError: If Quran data is not loaded
        """
        if not quran_service.is_loaded:
            logger.error("Attempted to generate schedule before loading Quran data")
            raise RuntimeError("Quran data not loaded")

        logger.info(
            f"Generating schedule: {settings.pages_per_period} pages per {settings.period_type}, "
            f"starting from page {settings.start_page}, order: {settings.order}"
        )

        # Get all pages
        all_pages = quran_service.get_all_pages()

        # Generate page sequence based on order
        page_sequence = self._generate_page_sequence(
            start_page=settings.start_page,
            order=settings.order,
            total_pages=len(all_pages)
        )

        # Group pages into periods
        schedule = self._create_period_schedule(
            page_sequence=page_sequence,
            pages_per_period=settings.pages_per_period,
            period_type=settings.period_type,
            all_pages=all_pages
        )

        logger.info(f"Generated schedule with {len(schedule)} periods")
        return schedule

    def _generate_page_sequence(
        self,
        start_page: int,
        order: str,
        total_pages: int
    ) -> List[int]:
        """
        Generate the sequence of pages to memorize based on order.

        Args:
            start_page: Starting page number (1-604)
            order: "Ascending" or "Descending"
            total_pages: Total number of pages (604)

        Returns:
            List of page numbers in the correct order
        """
        if order == "Ascending":
            # Start at start_page and go towards 604
            sequence = list(range(start_page, total_pages + 1))
        else:  # Descending
            # Start at start_page and go backwards to 1
            sequence = list(range(start_page, 0, -1))

        logger.debug(f"Generated page sequence: {len(sequence)} pages from {sequence[0]} to {sequence[-1]}")
        return sequence

    def _create_period_schedule(
        self,
        page_sequence: List[int],
        pages_per_period: int,
        period_type: str,
        all_pages: List[PageData]
    ) -> List[Dict]:
        """
        Create the schedule by grouping pages into periods.

        Args:
            page_sequence: Sequence of page numbers
            pages_per_period: Number of pages per period
            period_type: "Daily" or "Weekly"
            all_pages: All Quran pages data

        Returns:
            List of period schedule dictionaries
        """
        schedule = []
        period_number = 1

        # Group pages into chunks
        for i in range(0, len(page_sequence), pages_per_period):
            period_pages = page_sequence[i:i + pages_per_period]

            # Get page data for this period
            page_data_list = [all_pages[page_num - 1] for page_num in period_pages]

            # Extract unique surahs and juzs
            surahs_en, surahs_ar = self._extract_unique_surahs(page_data_list)
            juzs = self._extract_unique_juzs(page_data_list)

            # Create page range string
            if len(period_pages) == 1:
                page_range = str(period_pages[0])
            else:
                page_range = f"{period_pages[0]}-{period_pages[-1]}"

            # Create period label (in French)
            period_label = f"{'Jour' if period_type == 'Daily' else 'Semaine'} {period_number}"

            schedule.append({
                "period_label": period_label,
                "page_range": page_range,
                "surahs_en": surahs_en,
                "surahs_ar": surahs_ar,
                "juzs": juzs
            })

            period_number += 1

        return schedule

    def _extract_unique_surahs(self, page_data_list: List[PageData]) -> tuple[List[str], List[str]]:
        """
        Extract unique Surah names from page data.

        Args:
            page_data_list: List of page data

        Returns:
            Tuple of (English names list, Arabic names list)
        """
        surah_map = {}  # Map english name to arabic name
        for page in page_data_list:
            for ayah in page.ayahs:
                surah_map[ayah.surah.englishName] = ayah.surah.name

        sorted_english = sorted(surah_map.keys())
        sorted_arabic = [surah_map[en] for en in sorted_english]

        return sorted_english, sorted_arabic

    def _extract_unique_juzs(self, page_data_list: List[PageData]) -> List[int]:
        """
        Extract unique Juz numbers from page data.

        Args:
            page_data_list: List of page data

        Returns:
            List of unique Juz numbers
        """
        juzs = set()
        for page in page_data_list:
            for ayah in page.ayahs:
                juzs.add(ayah.juz)

        return sorted(list(juzs))


# Global service instance
planning_service = PlanningService()
