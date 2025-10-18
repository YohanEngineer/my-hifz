"""
Unit tests for QuranService.
"""

import json
import pytest
from pathlib import Path
from app.services.quran_service import QuranService
from app.models import PageData


@pytest.fixture
def temp_quran_data(tmp_path):
    """Create a temporary Quran data file for testing."""
    data = [
        {
            "number": 1,
            "topPageSurah": {
                "number": 1,
                "name": "سورة الفاتحة",
                "englishName": "Al-Faatiha",
                "englishNameTranslation": "The Opening",
                "revelationType": "Meccan",
                "numberOfAyahs": 7
            },
            "hizbNumbers": [1],
            "ayahs": [
                {
                    "number": 1,
                    "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                    "surah": {
                        "number": 1,
                        "name": "سورة الفاتحة",
                        "englishName": "Al-Faatiha",
                        "englishNameTranslation": "The Opening",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 7
                    },
                    "numberInSurah": 1,
                    "juz": 1,
                    "manzil": 1,
                    "page": 1,
                    "ruku": 1,
                    "hizbQuarter": 1,
                    "sajda": False
                }
            ]
        },
        {
            "number": 2,
            "topPageSurah": {
                "number": 2,
                "name": "سورة البقرة",
                "englishName": "Al-Baqara",
                "englishNameTranslation": "The Cow",
                "revelationType": "Medinan",
                "numberOfAyahs": 286
            },
            "hizbNumbers": [1],
            "ayahs": [
                {
                    "number": 8,
                    "text": "الم",
                    "surah": {
                        "number": 2,
                        "name": "سورة البقرة",
                        "englishName": "Al-Baqara",
                        "englishNameTranslation": "The Cow",
                        "revelationType": "Medinan",
                        "numberOfAyahs": 286
                    },
                    "numberInSurah": 1,
                    "juz": 1,
                    "manzil": 1,
                    "page": 2,
                    "ruku": 1,
                    "hizbQuarter": 1,
                    "sajda": False
                }
            ]
        }
    ]

    json_file = tmp_path / "test_quran.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    return json_file


class TestQuranService:
    """Tests for QuranService class."""

    def test_load_data_success(self, temp_quran_data):
        """Test successfully loading Quran data."""
        service = QuranService()
        service.load_data(temp_quran_data)

        assert service.is_loaded
        assert service.page_count == 2

    def test_load_data_file_not_found(self):
        """Test loading data from non-existent file."""
        service = QuranService()

        with pytest.raises(FileNotFoundError):
            service.load_data(Path("non_existent.json"))

    def test_get_all_pages(self, temp_quran_data):
        """Test retrieving all pages."""
        service = QuranService()
        service.load_data(temp_quran_data)

        pages = service.get_all_pages()
        assert len(pages) == 2
        assert isinstance(pages[0], PageData)

    def test_get_all_pages_not_loaded(self):
        """Test getting all pages before data is loaded."""
        service = QuranService()

        with pytest.raises(RuntimeError):
            service.get_all_pages()

    def test_get_page_valid(self, temp_quran_data):
        """Test retrieving a valid page."""
        service = QuranService()
        service.load_data(temp_quran_data)

        page = service.get_page(1)
        assert page is not None
        assert page.number == 1
        assert page.topPageSurah.englishName == "Al-Faatiha"

    def test_get_page_invalid_number(self, temp_quran_data):
        """Test retrieving a page with invalid number."""
        service = QuranService()
        service.load_data(temp_quran_data)

        page = service.get_page(0)
        assert page is None

        page = service.get_page(605)
        assert page is None

    def test_get_page_not_loaded(self):
        """Test getting a page before data is loaded."""
        service = QuranService()

        with pytest.raises(RuntimeError):
            service.get_page(1)

    def test_get_pages_by_surah(self, temp_quran_data):
        """Test retrieving pages by Surah number."""
        service = QuranService()
        service.load_data(temp_quran_data)

        pages = service.get_pages_by_surah(1)
        assert len(pages) == 1
        assert pages[0].number == 1

    def test_get_pages_by_surah_invalid(self, temp_quran_data):
        """Test retrieving pages with invalid Surah number."""
        service = QuranService()
        service.load_data(temp_quran_data)

        pages = service.get_pages_by_surah(0)
        assert pages == []

        pages = service.get_pages_by_surah(115)
        assert pages == []

    def test_get_pages_by_juz(self, temp_quran_data):
        """Test retrieving pages by Juz number."""
        service = QuranService()
        service.load_data(temp_quran_data)

        pages = service.get_pages_by_juz(1)
        assert len(pages) == 2

    def test_get_pages_by_juz_invalid(self, temp_quran_data):
        """Test retrieving pages with invalid Juz number."""
        service = QuranService()
        service.load_data(temp_quran_data)

        pages = service.get_pages_by_juz(0)
        assert pages == []

        pages = service.get_pages_by_juz(31)
        assert pages == []

    def test_is_loaded_property(self, temp_quran_data):
        """Test is_loaded property."""
        service = QuranService()
        assert not service.is_loaded

        service.load_data(temp_quran_data)
        assert service.is_loaded

    def test_page_count_property(self, temp_quran_data):
        """Test page_count property."""
        service = QuranService()
        assert service.page_count == 0

        service.load_data(temp_quran_data)
        assert service.page_count == 2
