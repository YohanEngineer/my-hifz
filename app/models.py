"""
Pydantic models for My Hifz Planner API.
Contains data models for Quran pages, ayahs, and surah information.
"""

from typing import List, Union, Literal
from pydantic import BaseModel, Field, field_validator


class SurahInfo(BaseModel):
    """Information about a Surah (chapter) of the Quran."""
    number: int
    name: str
    englishName: str
    englishNameTranslation: str
    revelationType: str
    numberOfAyahs: int


class Ayah(BaseModel):
    """A single verse (ayah) of the Quran."""
    number: int
    text: str
    surah: SurahInfo
    numberInSurah: int
    juz: int
    manzil: int
    page: int
    ruku: int
    hizbQuarter: int
    sajda: Union[bool, int]  # Can be False or sajda number (1-15)


class PageData(BaseModel):
    """A single page of the Quran with all its ayahs."""
    number: int
    topPageSurah: SurahInfo
    hizbNumbers: List[int]
    ayahs: List[Ayah]


class PlanningSettings(BaseModel):
    """Settings for generating a memorization schedule."""
    pages_per_period: int = Field(..., gt=0, description="Number of pages to memorize per period")
    period_type: Literal["Daily", "Weekly"] = Field(..., description="Type of period: Daily or Weekly")
    start_page: int = Field(..., ge=1, le=604, description="Starting page number (1-604)")
    order: Literal["Ascending", "Descending"] = Field(..., description="Order of memorization: Ascending or Descending")


class PeriodSchedule(BaseModel):
    """Schedule for a single period (day or week)."""
    period_label: str = Field(..., description="Label for the period (e.g., 'Day 1', 'Week 5')")
    page_range: str = Field(..., description="Page range for this period (e.g., '50-51')")
    surahs_en: List[str] = Field(..., description="List of unique English Surah names")
    juzs: List[int] = Field(..., description="List of unique Juz numbers")
