#!/usr/bin/env python3
"""
Scrape Independiente matches from josecarluccio.blogspot.com
Scrapes years 1905-2019 and saves to data/YYYY.csv files
"""

import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import time

BASE_URL = "https://josecarluccio.blogspot.com/search/label/"
OUTPUT_DIR = "data"

def fetch(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        return None

def parse_match_line(line, competition=""):
    """
    Parse match lines. Handles multiple formats:
    - 04/04/1936 en Avellaneda: Independiente 5, Barracas Central 1
    - 04/04/1936 en Avellaneda: Independiente 5 - 1 Barracas Central
    - 04/04/1936: Independiente 5, Barracas Central 1
    """
    line = line.strip()
    if not line:
        return None
    
    # Skip lines that don't have dates
    if not re.match(r'\d{2}/\d{2}/\d{4}', line):
        return None
    
    # Pattern 1: "date en location: Team1 X, Team2 Y"
    pattern1 = r'(\d{2}/\d{2}/\d{4})\s+en\s+[^:]+:\s*([^,\d][^,]*?)(\d+)\s*,\s*([^,\d][^,]*?)(\d+)\s*$'
    
    # Pattern 2: "date: Team1 X, Team2 Y" (without location)
    pattern2 = r'(\d{2}/\d{2}/\d{4})\s*:\s*([^,\d][^,]*?)(\d+)\s*,\s*([^,\d][^,]*?)(\d+)\s*$'
    
    # Pattern 3: "date en location: Team1 X - Y Team2" (dash format)
    pattern3 = r'(\d{2}/\d{2}/\d{4})\s+en\s+[^:]+:\s*([^\d]+?)(\d+)\s*-\s*(\d+)\s*([^\d].*?)$'
    
    match = None
    date = team1 = score1 = team2 = score2 = None
    
    # Try pattern 1
    m = re.search(pattern1, line)
    if m:
        date, team1, score1, team2, score2 = m.groups()
    else:
        # Try pattern 2
        m = re.search(pattern2, line)
        if m:
            date, team1, score1, team2, score2 = m.groups()
        else:
            # Try pattern 3
            m = re.search(pattern3, line)
            if m:
                date, team1, score1, score2, team2 = m.groups()
    
    if not m:
        return None
    
    team1 = team1.strip()
    team2 = team2.strip()
    t1_lower = team1.lower()
    t2_lower = team2.lower()
    
    # Check if Independiente is in this match
    if 'independiente' not in t1_lower and 'independiente' not in t2_lower:
        return None
    
    # Determine home/away and result
    if 'independiente' in t1_lower:
        home_team, away_team = team1, team2
        home_score, away_score = score1, score2
        try:
            hs, as_ = int(home_score), int(away_score)
            result = "WIN" if hs > as_ else "LOSS" if hs < as_ else "DRAW"
        except:
            result = "UNKNOWN"
    else:
        home_team, away_team = team1, team2
        home_score, away_score = score1, score2
        try:
            hs, as_ = int(home_score), int(away_score)
            result = "WIN" if as_ > hs else "LOSS" if as_ < hs else "DRAW"
        except:
            result = "UNKNOWN"
    
    return {
        'date': date,
        'competition': competition,
        'home_team': home_team,
        'away_team': away_team,
        'home_score': str(home_score),
        'away_score': str(away_score),
        'result': result
    }

def extract_competition(title):
    """Extract competition from post title"""
    t = title.lower()
    
    # Copa competitions
    if 'copa libertadores' in t:
        return 'Copa Libertadores'
    elif 'copa sudamericana' in t:
        return 'Copa Sudamericana'
    elif 'copa de honor' in t:
        return 'Copa de Honor'
    elif 'copa competencia' in t:
        return 'Copa Competencia'
    elif 'copa ibarguren' in t:
        return 'Copa Ibarguren'
    elif 'copa argentina' in t:
        return 'Copa Argentina'
    elif 'copa' in t and ('rosario' in t or 'reyna' in t):
        return 'Copa'
    
    # Division competitions
    elif '1ra' in t or 'primera division' in t:
        return '1ra. División'
    elif '2da' in t or 'segunda division' in t:
        return '2da. División'
    elif '3ra' in t or 'tercera division' in t:
        return '3ra. División'
    elif 'primera b' in t:
        return 'Primera B'
    elif 'metropolitano' in t:
        return 'Metropolitano'
    elif 'nacional' in t:
        return 'Nacional'
    
    # Tournament names
    elif 'apertura' in t:
        return 'Torneo Apertura'
    elif 'clausura' in t:
        return 'Torneo Clausura'
    elif 'inicial' in t:
        return 'Torneo Inicial'
    elif 'final' in t:
        return 'Torneo Final'
    elif 'campeonato' in t:
        return 'Campeonato'
    elif 'torneo' in t:
        return 'Torneo'
    
    return 'Torneo'

def scrape_year(year):
    """Scrape all matches for a specific year"""
    url = f"{BASE_URL}{year}"
    soup = fetch(url)
    
    if not soup:
        return []
    
    matches = []
    
    # Find all post titles
    post_titles = soup.find_all('h3', class_='post-title')
    
    for title_elem in post_titles:
        a_tag = title_elem.find('a')
        if not a_tag or not a_tag.get('href'):
            continue
        
        title = a_tag.get_text(strip=True)
        post_url = a_tag['href']
        
        # Skip if not a tournament post
        if not any(x in title.lower() for x in ['copa', 'campeonato', 'torneo', 'division', 'primera', 'apertura', 'clausura', 'metropolitano', 'nacional']):
            continue
        
        competition = extract_competition(title)
        
        # Fetch post content
        post_soup = fetch(post_url)
        if not post_soup:
            continue
        
        post_body = post_soup.find('div', class_='post-body')
        if not post_body:
            continue
        
        text = post_body.get_text()
        
        # Check if Independiente is mentioned
        if 'independiente' not in text.lower():
            continue
        
        # Parse match lines
        lines = text.split('\n')
        for line in lines:
            match = parse_match_line(line, competition)
            if match:
                matches.append(match)
    
    return matches

def save_to_csv(year, matches):
    """Save matches to CSV, avoiding duplicates"""
    if not matches:
        return 0
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = os.path.join(OUTPUT_DIR, f"{year}.csv")
    
    # Read existing matches
    existing = set()
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.add((row['date'], row['home_team'], row['away_team']))
    
    # Filter new matches
    new_matches = [m for m in matches if (m['date'], m['home_team'], m['away_team']) not in existing]
    
    if not new_matches:
        return 0
    
    # Write to CSV
    file_exists = os.path.exists(filename)
    with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_matches)
    
    return len(new_matches)

def main():
    print("="*60)
    print("Independiente Match Scraper (1905-2019)")
    print("="*60)
    
    total = 0
    
    for year in range(1905, 2020):
        try:
            print(f"\nScraping {year}...", end=" ")
            matches = scrape_year(year)
            saved = save_to_csv(year, matches)
            print(f"found {len(matches)}, saved {saved} new")
            total += saved
            
            # Be polite - wait between requests
            time.sleep(1)
            
        except Exception as e:
            print(f"\nError in {year}: {e}")
            continue
    
    print("\n" + "="*60)
    print(f"Complete! Total new matches: {total}")
    print(f"Data saved to: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
