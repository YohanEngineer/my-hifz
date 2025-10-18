#!/usr/bin/env python3
"""
Script to fetch Quran page data from quranhub.com API and generate quran.json
Fetches all 604 pages of the Quran with their Surah and Juz information.
"""

import requests
import json
import time
from typing import List, Dict, Any


def fetch_page_data(page_number: int) -> Dict[str, Any]:
    """
    Fetch data for a single Quran page from the API.

    Args:
        page_number: Page number to fetch (1-604)

    Returns:
        Dictionary containing page data
    """
    url = f"https://api.quranhub.com/v1/page/{page_number}"
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        raise


def fetch_all_pages(total_pages: int = 604, delay: float = 0.1) -> List[Dict[str, Any]]:
    """
    Fetch all Quran pages from the API.

    Args:
        total_pages: Total number of pages to fetch (default: 604)
        delay: Delay between requests in seconds to avoid rate limiting

    Returns:
        List of page data dictionaries
    """
    all_pages = []

    print(f"Fetching {total_pages} pages from Quran API...")

    for page_num in range(1, total_pages + 1):
        try:
            page_data = fetch_page_data(page_num)
            all_pages.append(page_data)

            # Progress indicator
            if page_num % 50 == 0:
                print(f"Progress: {page_num}/{total_pages} pages fetched")

            # Small delay to be respectful to the API
            time.sleep(delay)

        except Exception as e:
            print(f"Failed to fetch page {page_num}. Stopping.")
            raise

    print(f"Successfully fetched all {total_pages} pages!")
    return all_pages


def save_to_json(data: List[Dict[str, Any]], filename: str = "quran.json") -> None:
    """
    Save the fetched data to a JSON file.

    Args:
        data: List of page data to save
        filename: Output filename (default: quran.json)
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Data saved to {filename}")


def main():
    """Main execution function."""
    try:
        # Fetch all pages
        pages_data = fetch_all_pages(total_pages=604, delay=0.1)

        # Save to JSON file
        save_to_json(pages_data, "quran.json")

        # Print summary
        print(f"\n✓ Successfully created quran.json with {len(pages_data)} pages")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
