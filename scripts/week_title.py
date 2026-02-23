#!/usr/bin/env python3
"""
Generate week title and filename for news posts.
Usage: python scripts/week_title.py [YYYY-MM-DD]
If no date provided, uses current date.
"""

import sys
from datetime import datetime

def get_week_info(date_str=None):
    """
    Calculate week number within the month and generate title.

    Args:
        date_str: Date string in YYYY-MM-DD format (optional)

    Returns:
        dict with title, filename, month, year, week_num
    """
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.now()

    # Calculate week number within the month (1-indexed)
    week_num = ((date.day - 1) // 7) + 1

    month_name = date.strftime("%B")  # Full month name
    year = date.year

    # Generate title: "February 2026, Week 2"
    title = f"{month_name} {year}, Week {week_num}"

    # Generate filename: 2026-02-week-2.md
    month_num = date.strftime('%m')
    filename = f"{year}-{month_num}-week-{week_num}.md"

    return {
        "title": title,
        "filename": filename,
        "month": month_name,
        "year": year,
        "week_num": week_num,
        "date": date.strftime("%Y-%m-%d")
    }

if __name__ == "__main__":
    date_str = sys.argv[1] if len(sys.argv) > 1 else None
    info = get_week_info(date_str)

    # Print in a format easy to parse
    print(f"Title: {info['title']}")
    print(f"Filename: {info['filename']}")
    print(f"Month: {info['month']}")
    print(f"Year: {info['year']}")
    print(f"Week: {info['week_num']}")
    print(f"Date: {info['date']}")
