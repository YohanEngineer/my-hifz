"""
Unit tests for Pydantic models.
"""

import pytest
from app.models import SurahInfo, Ayah, PageData


class TestSurahInfo:
    """Tests for SurahInfo model."""

    def test_surah_info_creation(self):
        """Test creating a valid SurahInfo instance."""
        surah = SurahInfo(
            number=1,
            name="سورة الفاتحة",
            englishName="Al-Faatiha",
            englishNameTranslation="The Opening",
            revelationType="Meccan",
            numberOfAyahs=7
        )
        assert surah.number == 1
        assert surah.englishName == "Al-Faatiha"
        assert surah.numberOfAyahs == 7

    def test_surah_info_validation(self):
        """Test SurahInfo validation."""
        with pytest.raises(ValueError):
            SurahInfo(
                number="invalid",  # Should be int
                name="Test",
                englishName="Test",
                englishNameTranslation="Test",
                revelationType="Meccan",
                numberOfAyahs=7
            )


class TestAyah:
    """Tests for Ayah model."""

    def test_ayah_creation_with_bool_sajda(self):
        """Test creating an Ayah with boolean sajda."""
        surah = SurahInfo(
            number=1,
            name="سورة الفاتحة",
            englishName="Al-Faatiha",
            englishNameTranslation="The Opening",
            revelationType="Meccan",
            numberOfAyahs=7
        )

        ayah = Ayah(
            number=1,
            text="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
            surah=surah,
            numberInSurah=1,
            juz=1,
            manzil=1,
            page=1,
            ruku=1,
            hizbQuarter=1,
            sajda=False
        )

        assert ayah.number == 1
        assert ayah.sajda is False

    def test_ayah_creation_with_int_sajda(self):
        """Test creating an Ayah with integer sajda number."""
        surah = SurahInfo(
            number=7,
            name="سورة الأعراف",
            englishName="Al-A'raaf",
            englishNameTranslation="The Heights",
            revelationType="Meccan",
            numberOfAyahs=206
        )

        ayah = Ayah(
            number=206,
            text="إِنَّ الَّذِينَ عِندَ رَبِّكَ لَا يَسْتَكْبِرُونَ عَنْ عِبَادَتِهِ وَيُسَبِّحُونَهُ وَلَهُ يَسْجُدُونَ",
            surah=surah,
            numberInSurah=206,
            juz=9,
            manzil=3,
            page=176,
            ruku=24,
            hizbQuarter=70,
            sajda=1  # Sajda number
        )

        assert ayah.sajda == 1


class TestPageData:
    """Tests for PageData model."""

    def test_page_data_creation(self):
        """Test creating a valid PageData instance."""
        surah = SurahInfo(
            number=1,
            name="سورة الفاتحة",
            englishName="Al-Faatiha",
            englishNameTranslation="The Opening",
            revelationType="Meccan",
            numberOfAyahs=7
        )

        ayah = Ayah(
            number=1,
            text="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
            surah=surah,
            numberInSurah=1,
            juz=1,
            manzil=1,
            page=1,
            ruku=1,
            hizbQuarter=1,
            sajda=False
        )

        page = PageData(
            number=1,
            topPageSurah=surah,
            hizbNumbers=[1],
            ayahs=[ayah]
        )

        assert page.number == 1
        assert page.topPageSurah.englishName == "Al-Faatiha"
        assert len(page.ayahs) == 1
        assert len(page.hizbNumbers) == 1
