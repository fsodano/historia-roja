#!/usr/bin/env python3
"""
Extract Independiente matches from josecarluccio.blogspot.com
Creates 1 CSV file per year: data/YYYY.csv
"""

import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import time

BASE_URL = "https://josecarluccio.blogspot.com"
DATA_DIR = "data"

def fetch(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        print(f"    Error fetching {url}: {e}")
        return None

def get_valid_years():
    """Extract all valid year labels from the sidebar"""
    print("Extracting valid years from sidebar...")
    soup = fetch(BASE_URL)
    if not soup:
        return []
    
    years = []
    labels = soup.find_all('a', href=re.compile(r'/search/label/'))
    
    for label in labels:
        href = label.get('href', '')
        match = re.search(r'/search/label/(\d{4})', href)
        if match:
            year = int(match.group(1))
            if 1891 <= year <= 2019:
                years.append(year)
    
    years = sorted(set(years))
    print(f"Found {len(years)} valid years: {years[0]}-{years[-1]}")
    return years

def parse_match_line(line, competition=""):
    """Parse a match line with format: date en location: Team1 X, Team2 Y"""
    line = line.strip()
    if not line:
        return None
    
    # Pattern: DD/MM/YYYY en location: Team1 score1, Team2 score2
    pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+[^:]+:\s*([^,]+?)(\d+)\s*,\s*([^,]+?)(\d+)\s*$'
    m = re.search(pattern, line)
    
    if not m:
        return None
    
    date, team1, score1, team2, score2 = m.groups()
    team1 = team1.strip()
    team2 = team2.strip()
    
    # Check if Independiente is in this match
    t1_lower = team1.lower()
    t2_lower = team2.lower()
    
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
            result = "DRAW"
    else:
        home_team, away_team = team1, team2
        home_score, away_score = score1, score2
        try:
            hs, as_ = int(home_score), int(away_score)
            result = "WIN" if as_ > hs else "LOSS" if as_ < hs else "DRAW"
        except:
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

def extract_competition(title):
    """Extract competition name from post title"""
    t = title.lower()
    
    competitions = [
        (r'1ra\.?\s*divisi[oó]n', '1ra. División'),
        (r'2da\.?\s*divisi[oó]n', '2da. División'),
        (r'3ra\.?\s*divisi[oó]n', '3ra. División'),
        (r'primera\s+b\s*nacional', 'Primera B Nacional'),
        (r'copa\s+libertadores', 'Copa Libertadores'),
        (r'copa\s+sudamericana', 'Copa Sudamericana'),
        (r'copa\s+argentina', 'Copa Argentina'),
        (r'copa\s+de\s+honor', 'Copa de Honor'),
        (r'copa\s+competencia', 'Copa Competencia'),
        (r'copa\s+ibarguren', 'Copa Ibarguren'),
        (r'copa\s+mariano\s+reyna', 'Copa Mariano Reyna'),
        (r'copas?\s+interligas', 'Copas Interligas'),
        (r'campeonato\s+rioplatense', 'Campeonato Rioplatense'),
        (r'campeonato\s+argentino\s+interligas', 'Campeonato Argentino Interligas'),
        (r'torneo\s+apertura', 'Torneo Apertura'),
        (r'torneo\s+clausura', 'Torneo Clausura'),
        (r'torneo\s+inicial', 'Torneo Inicial'),
        (r'torneo\s+final', 'Torneo Final'),
        (r'torneo\s+preparaci[oó]n', 'Torneo Preparación'),
        (r'torneo\s+reducido', 'Torneo Reducido'),
        (r'campeonato', 'Campeonato'),
        (r'torneo', 'Torneo'),
    ]
    
    for pattern, name in competitions:
        if re.search(pattern, t):
            return name
    
    return 'Torneo'

def scrape_year(year):
    """Scrape all Independiente matches for a specific year"""
    url = f"{BASE_URL}/search/label/{year}"
    print(f"\nScraping year {year}...")
    
    soup = fetch(url)
    if not soup:
        print(f"  Failed to fetch year {year}")
        return []
    
    matches = []
    
    # Find all post titles
    post_titles = soup.find_all('h3', class_='post-title')
    print(f"  Found {len(post_titles)} posts")
    
    for title_elem in post_titles:
        a_tag = title_elem.find('a')
        if not a_tag or not a_tag.get('href'):
            continue
        
        title = a_tag.get_text(strip=True)
        post_url = a_tag['href']
        
        # Extract competition from title
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
        
        # Parse each line for match data
        for line in text.split('\n'):
            match = parse_match_line(line, competition)
            if match:
                matches.append(match)
    
    print(f"  Found {len(matches)} Independiente matches")
    return matches

def save_year_csv(year, matches):
    """Save matches to a year-specific CSV file"""
    if not matches:
        return
    
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = os.path.join(DATA_DIR, f"{year}.csv")
    
    # Remove duplicates based on date + teams
    seen = set()
    unique_matches = []
    for m in matches:
        key = (m['date'], m['home_team'], m['away_team'])
        if key not in seen:
            seen.add(key)
            unique_matches.append(m)
    
    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        writer.writeheader()
        writer.writerows(unique_matches)
    
    print(f"  Saved {len(unique_matches)} matches to {filename}")

def main():
    print("="*60)
    print("Independiente Match Extractor")
    print("Creates 1 CSV file per year")
    print("="*60)
    
    # Get all valid years
    years = get_valid_years()
    
    if not years:
        print("No valid years found!")
        return
    
    print(f"\nWill scrape {len(years)} years...")
    print()
    
    total_matches = 0
    
    for year in years:
        matches = scrape_year(year)
        save_year_csv(year, matches)
        total_matches += len(matches)
        
        # Be polite - wait between requests
        time.sleep(1)
    
    print("\n" + "="*60)
    print(f"COMPLETE!")
    print(f"Total matches extracted: {total_matches}")
    print(f"Files saved to: {DATA_DIR}/")
    print("="*60)

if __name__ == "__main__":
    main()
