#!/usr/bin/env python3
"""
Master scraper for all Independiente matches from josecarluccio.blogspot.com
Scrapes years 1891-2019 and saves to data/YYYY.csv files
"""

import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import time
import sys

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
        (r'torneo', 'Torneo'),
        (r'campeonato', 'Campeonato'),
    ]
    
    for pattern, name in competitions:
        if re.search(pattern, t):
            return name
    
    return 'Torneo'

def scrape_year(year):
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
    years = list(range(1891, 2020))
    total = 0
    
    print("="*60)
    print("Independiente Match Scraper (1891-2019)")
    print("="*60)
    print(f"Scraping {len(years)} years...")
    print()
    
    for i, year in enumerate(years, 1):
        print(f"[{i}/{len(years)}] Year {year}...", end=" ", flush=True)
        matches = scrape_year(year)
        count = save_year_csv(year, matches)
        print(f"found {len(matches)}, saved {count}")
        total += count
        time.sleep(1)
    
    print()
    print("="*60)
    print(f"COMPLETE!")
    print(f"Total matches: {total}")
    print(f"Files saved to: {DATA_DIR}/")
    print("="*60)

if __name__ == "__main__":
    main()
