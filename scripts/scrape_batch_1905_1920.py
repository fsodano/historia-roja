#!/usr/bin/env python3
"""
Scrape Independiente matches for years 1905-1920
Saves to individual CSV files per year
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
        return None

def parse_match_line(line, competition=""):
    """Parse match line: date en location: Team1 X, Team2 Y"""
    line = line.strip()
    if not line:
        return None
    
    pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+[^:]+:\s*([^,]+?)(\d+)\s*,\s*([^,]+?)(\d+)\s*$'
    m = re.search(pattern, line)
    
    if not m:
        return None
    
    date, team1, score1, team2, score2 = m.groups()
    team1 = team1.strip()
    team2 = team2.strip()
    
    if 'independiente' not in team1.lower() and 'independiente' not in team2.lower():
        return None
    
    if 'independiente' in team1.lower():
        home, away = team1, team2
        hs, as_ = score1, score2
        try:
            result = "WIN" if int(hs) > int(as_) else "LOSS" if int(hs) < int(as_) else "DRAW"
        except:
            result = "DRAW"
    else:
        home, away = team1, team2
        hs, as_ = score1, score2
        try:
            result = "WIN" if int(as_) > int(hs) else "LOSS" if int(as_) < int(hs) else "DRAW"
        except:
            result = "DRAW"
    
    return {
        'date': date,
        'competition': competition,
        'home_team': home,
        'away_team': away,
        'home_score': hs,
        'away_score': as_,
        'result': result
    }

def extract_competition(title):
    """Extract competition from post title"""
    t = title.lower()
    if '1ra' in t:
        return '1ra. División'
    elif '2da' in t:
        return '2da. División'
    elif '3ra' in t:
        return '3ra. División'
    elif 'copa de honor' in t:
        return 'Copa de Honor'
    elif 'copa competencia' in t:
        return 'Copa Competencia'
    elif 'copa ibarguren' in t:
        return 'Copa Ibarguren'
    elif 'copa' in t:
        return 'Copa'
    elif 'campeonato' in t:
        return 'Campeonato'
    elif 'torneo' in t:
        return 'Torneo'
    return 'Torneo'

def scrape_year(year):
    """Scrape a single year"""
    url = f"{BASE_URL}/search/label/{year}"
    soup = fetch(url)
    
    if not soup:
        return []
    
    matches = []
    posts = soup.find_all('h3', class_='post-title')
    
    for post in posts:
        a = post.find('a')
        if not a or not a.get('href'):
            continue
        
        title = a.get_text(strip=True)
        competition = extract_competition(title)
        
        post_soup = fetch(a['href'])
        if not post_soup:
            continue
        
        body = post_soup.find('div', class_='post-body')
        if not body:
            continue
        
        text = body.get_text()
        if 'independiente' not in text.lower():
            continue
        
        for line in text.split('\n'):
            match = parse_match_line(line, competition)
            if match:
                matches.append(match)
    
    return matches

def save_year_csv(year, matches):
    """Save matches to CSV"""
    if not matches:
        return 0
    
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = os.path.join(DATA_DIR, f"{year}.csv")
    
    seen = set()
    unique = []
    for m in matches:
        key = (m['date'], m['home_team'], m['away_team'])
        if key not in seen:
            seen.add(key)
            unique.append(m)
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        w.writeheader()
        w.writerows(unique)
    
    return len(unique)

def main():
    years = list(range(1905, 1921))
    total = 0
    
    print(f"Scraping years {years[0]}-{years[-1]}")
    print("=" * 50)
    
    for year in years:
        print(f"\nYear {year}...", end=" ")
        matches = scrape_year(year)
        count = save_year_csv(year, matches)
        print(f"found {len(matches)}, saved {count}")
        total += count
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print(f"Total: {total} matches")

if __name__ == "__main__":
    main()
