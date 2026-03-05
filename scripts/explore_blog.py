#!/usr/bin/env python3
"""Explore blog structure for Independiente matches"""

import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://josecarluccio.blogspot.com/search/label/"

def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error: {e}")
        return None

# Explore one of the posts in detail
url = "https://josecarluccio.blogspot.com/2015/06/argentina-1ra-division-afa-torneo.html"
print(f"Exploring: {url}")
print("=" * 80)

soup = fetch_page(url)
if soup:
    # Get all text content
    text = soup.get_text()
    
    # Find all tables
    tables = soup.find_all('table')
    print(f"\nFound {len(tables)} tables")
    
    # Look for Independiente mentions
    lines = text.split('\n')
    independiente_lines = []
    for line in lines:
        line = line.strip()
        if 'independiente' in line.lower() and len(line) > 10:
            independiente_lines.append(line)
    
    print(f"\nFound {len(independiente_lines)} lines mentioning Independiente:")
    for i, line in enumerate(independiente_lines[:30]):
        print(f"{i+1}. {line}")
    
    # Look for patterns like scores
    print("\n\nLooking for score patterns...")
    score_lines = []
    for line in lines:
        line = line.strip()
        if re.search(r'\d+\s*-\s*\d+', line) and len(line) > 5 and len(line) < 200:
            score_lines.append(line)
    
    print(f"Found {len(score_lines)} lines with scores:")
    for i, line in enumerate(score_lines[:30]):
        print(f"{i+1}. {line}")

