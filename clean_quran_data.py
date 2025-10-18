#!/usr/bin/env python3
"""
Script to clean the Quran JSON file by removing API metadata (code, status)
and keeping only the actual data.
"""

import json


def clean_quran_data(input_file: str = "quran.json", output_file: str = "quran.json"):
    """
    Remove API metadata from quran.json and keep only the data portion.

    Args:
        input_file: Input JSON file path
        output_file: Output JSON file path (will overwrite if same)
    """
    print(f"Reading {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    print(f"Cleaning {len(raw_data)} pages...")

    # Extract only the 'data' portion from each page
    cleaned_data = []
    for page in raw_data:
        if 'data' in page:
            cleaned_data.append(page['data'])
        else:
            # In case the structure is different
            print(f"Warning: No 'data' key found in page {page.get('number', 'unknown')}")
            cleaned_data.append(page)

    print(f"Writing cleaned data to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"✓ Successfully cleaned {len(cleaned_data)} pages")
    print(f"✓ Removed 'code' and 'status' fields from all pages")


if __name__ == "__main__":
    clean_quran_data()
