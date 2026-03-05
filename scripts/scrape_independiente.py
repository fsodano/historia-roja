#!/usr/bin/env python3
"""Scrape Independiente match data from josecarluccio.blogspot.com for years 1905-2019"""

import requests
from bs4 import BeautifulSoup
import re
import csv
import os
from datetime import datetime

BASE_URL = "https://josecarluccio.blogspot.com/search/label/"
OUTPUT_DIR = "data"

def ensure_dir():
    """Ensure output directory exists"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def fetch_page(url):
    """Fetch a page and return BeautifulSoup object"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None

def extract_match_line_data(line, competition=""):
    """Extract match data from a line with format: date en location: Team1 X, Team2 Y"""
    matches = []
    
    # Pattern: DD/MM/YYYY en location: Team1 X, Team2 Y
    # or variations like: date: Team1 X, Team2 Y
    patterns = [
        r'(\d{1,2}/\d{1,2}/\d{4})\s+en\s+[^:]+:\s*([^,\d]+?)(\d+)\s*,\s*([^,\d]+?)(\d+)',
        r'(\d{1,2}/\d{1,2}/\d{4})\s*:\s*([^,\d]+?)(\d+)\s*,\s*([^,\d]+?)(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            date = match.group(1)
            team1 = match.group(2).strip()
            score1 = match.group(3).strip()
            team2 = match.group(4).strip()
            score2 = match.group(5).strip()
            
            # Check if Independiente is in this match
            team1_lower = team1.lower()
            team2_lower = team2.lower()
            
            if 'independiente' in team1_lower or 'independiente' in team2_lower:
                # Determine home/away and result
                if 'independiente' in team1_lower:
                    home_team = team1
                    away_team = team2
                    home_score = score1
                    away_score = score2
                    
                    # Determine result from Independiente's perspective (home)
                    if int(score1) > int(score2):
                        result = "WIN"
                    elif int(score1) < int(score2):
                        result = "LOSS"
                    else:
                        result = "DRAW"
                else:
                    home_team = team1
                    away_team = team2
                    home_score = score1
                    away_score = score2
                    
                    # Determine result from Independiente's perspective (away)
                    if int(score2) > int(score1):
                        result = "WIN"
                    elif int(score2) < int(score1):
                        result = "LOSS"
                    else:
                        result = "DRAW"
                
                return {
                    'date': date,
                    'competition': competition,
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_score': home_score,
                    'away_score': away_score,
                    'result': result
                }
    
    return None

def extract_competition_name(title):
    """Extract competition name from post title"""
    title_lower = title.lower()
    
    competitions = [
        (r'1ra\.?\s*[división|division|cat]', '1ra. División'),
        (r'2da\.?\s*[división|division]', '2da. División'),
        (r'3ra\.?\s*[división|division]', '3ra. División'),
        (r'copas?\s+interligas', 'Copas Interligas'),
        (r'copa\s+de\s+honor', 'Copa de Honor'),
        (r'copa\s+competencia', 'Copa Competencia'),
        (r'copa\s+ibarguren', 'Copa Ibarguren'),
        (r'copa\s+[rosario|culacciati]', 'Copa Rosario'),
        (r'copa\s+mariano\s+reyna', 'Copa Mariano Reyna'),
        (r'campeonato\s+rioplatense', 'Campeonato Rioplatense'),
        (r'campeonato\s+argentino\s+interligas', 'Campeonato Argentino Interligas'),
        (r'torneo\s+preparaci[oó]n', 'Torneo Preparación'),
        (r'torneo\s+reducido', 'Torneo Reducido'),
        (r'copa\s+argentina', 'Copa Argentina'),
        (r'copa\s+libertadores', 'Copa Libertadores'),
        (r'copa\s+sudamericana', 'Copa Sudamericana'),
        (r'copa\s+de\s+la\s+liga', 'Copa de la Liga'),
        (r'supercopa', 'Supercopa'),
        (r'primera\s+b\s+nacional', 'Primera B Nacional'),
        (r'campeonato\s+amateur', 'Campeonato Amateur'),
    ]
    
    for pattern, name in competitions:
        if re.search(pattern, title_lower):
            return name
    
    # Default based on year
    if any(x in title_lower for x in ['primera', 'liga', 'apertura', 'clausura', 'metropolitano', 'nacional']):
        return 'Primera División'
    
    return 'Torneo'

def scrape_year_page(year):
    """Scrape all matches from a specific year label page"""
    url = f"{BASE_URL}{year}"
    print(f"\nScraping year {year}...")
    
    soup = fetch_page(url)
    if not soup:
        print(f"  Failed to fetch year {year}")
        return []
    
    matches = []
    
    # Get all post titles
    post_titles = soup.find_all('h3', class_='post-title')
    print(f"  Found {len(post_titles)} posts")
    
    for title in post_titles:
        title_text = title.get_text(strip=True)
        a_tag = title.find('a')
        
        if not a_tag:
            continue
            
        post_url = a_tag.get('href')
        if not post_url:
            continue
        
        # Extract competition name from title
        competition = extract_competition_name(title_text)
        
        # Fetch post content
        post_soup = fetch_page(post_url)
        if not post_soup:
            continue
        
        # Get post body text
        post_body = post_soup.find('div', class_='post-body')
        if not post_body:
            continue
        
        text = post_body.get_text()
        
        # Check if Independiente is mentioned
        if 'independiente' not in text.lower():
            continue
        
        # Split into lines and look for match patterns
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for match patterns
            match_data = extract_match_line_data(line, competition)
            if match_data:
                matches.append(match_data)
    
    print(f"  Found {len(matches)} Independiente matches")
    return matches

def save_to_csv(year, matches):
    """Save matches to year-specific CSV file"""
    if not matches:
        return
    
    filename = os.path.join(OUTPUT_DIR, f"{year}.csv")
    
    # Check for existing data to avoid duplicates
    existing = set()
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row['date'], row['home_team'], row['away_team'])
                existing.add(key)
    
    # Filter duplicates
    new_matches = []
    for m in matches:
        key = (m['date'], m['home_team'], m['away_team'])
        if key not in existing:
            new_matches.append(m)
            existing.add(key)
    
    if not new_matches:
        print(f"  No new matches to save")
        return
    
    # Write to CSV
    file_exists = os.path.exists(filename)
    with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_matches)
    
    print(f"  Saved {len(new_matches)} new matches to {filename}")

def main():
    ensure_dir()
    
    print("Starting Independiente match scraper (1905-2019)")
    print("=" * 60)
    
    total_matches = 0
    
    # Scrape years 1905-2019
    for year in range(1905, 2020):
        try:
            matches = scrape_year_page(year)
            save_to_csv(year, matches)
            total_matches += len(matches)
        except Exception as e:
            print(f"  Error processing year {year}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print(f"Scraping complete!")
    print(f"Total matches found: {total_matches}")
    print(f"Data saved to {OUTPUT_DIR}/ directory")

if __name__ == "__main__":
    main()
