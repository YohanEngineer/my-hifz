"""
Integration tests for API endpoints.
"""

import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from main import app
from app.services.quran_service import quran_service


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

    return data


@pytest.fixture
def client(temp_quran_data, tmp_path):
    """Create a test client with temporary data."""
    # Save temp data to file
    json_file = tmp_path / "quran.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(temp_quran_data, f, ensure_ascii=False)

    # Load data into service
    quran_service.load_data(json_file)

    return TestClient(app)


class TestRootEndpoints:
    """Tests for root endpoints."""

    def test_root(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["pages_loaded"] == 2


class TestQuranEndpoints:
    """Tests for Quran API endpoints."""

    def test_get_all_pages(self, client):
        """Test getting all pages."""
        response = client.get("/api/quran/pages")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 2
        assert data[0]["number"] == 1

    def test_get_page_valid(self, client):
        """Test getting a valid page."""
        response = client.get("/api/quran/pages/1")
        assert response.status_code == 200

        data = response.json()
        assert data["number"] == 1
        assert data["topPageSurah"]["englishName"] == "Al-Faatiha"
        assert len(data["ayahs"]) == 1

    def test_get_page_invalid_low(self, client):
        """Test getting a page with number too low."""
        response = client.get("/api/quran/pages/0")
        assert response.status_code == 400

        data = response.json()
        assert "Invalid page number" in data["detail"]

    def test_get_page_invalid_high(self, client):
        """Test getting a page with number too high."""
        response = client.get("/api/quran/pages/605")
        assert response.status_code == 400

        data = response.json()
        assert "Invalid page number" in data["detail"]

    def test_get_pages_by_surah_valid(self, client):
        """Test getting pages by valid Surah number."""
        response = client.get("/api/quran/pages/surah/1")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["number"] == 1

    def test_get_pages_by_surah_invalid(self, client):
        """Test getting pages by invalid Surah number."""
        response = client.get("/api/quran/pages/surah/0")
        assert response.status_code == 400

        response = client.get("/api/quran/pages/surah/115")
        assert response.status_code == 400

    def test_get_pages_by_surah_not_found(self, client):
        """Test getting pages by Surah number that has no pages."""
        response = client.get("/api/quran/pages/surah/50")
        assert response.status_code == 404

    def test_get_pages_by_juz_valid(self, client):
        """Test getting pages by valid Juz number."""
        response = client.get("/api/quran/pages/juz/1")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 2

    def test_get_pages_by_juz_invalid(self, client):
        """Test getting pages by invalid Juz number."""
        response = client.get("/api/quran/pages/juz/0")
        assert response.status_code == 400

        response = client.get("/api/quran/pages/juz/31")
        assert response.status_code == 400

    def test_get_pages_by_juz_not_found(self, client):
        """Test getting pages by Juz number that has no pages."""
        response = client.get("/api/quran/pages/juz/15")
        assert response.status_code == 404
