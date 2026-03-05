#!/usr/bin/env python3
"""
Parallel scraper for Independiente matches
Scrapes multiple years simultaneously
"""

import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import concurrent.futures
from datetime import datetime

BASE_URL = "https://josecarluccio.blogspot.com"
DATA_DIR = "data"
MAX_WORKERS = 5

def fetch(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return BeautifulSoup(r.content, 'html.parser')
    except:
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
    if '1ra' in t:
        return '1ra. División'
    elif '2da' in t:
        return '2da. División'
    elif 'copa libertadores' in t:
        return 'Copa Libertadores'
    elif 'copa sudamericana' in t:
        return 'Copa Sudamericana'
    elif 'copa argentina' in t:
        return 'Copa Argentina'
    elif 'copa' in t:
        return 'Copa'
    elif 'apertura' in t:
        return 'Torneo Apertura'
    elif 'clausura' in t:
        return 'Torneo Clausura'
    elif 'metropolitano' in t:
        return 'Metropolitano'
    elif 'nacional' in t:
        return 'Nacional'
    else:
        return 'Torneo'

def scrape_single_year(year):
    """Scrape a single year"""
    url = f"{BASE_URL}/search/label/{year}"
    soup = fetch(url)
    
    if not soup:
        return year, []
    
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
    
    return year, matches

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
    print("Parallel Independiente Scraper")
    print("=" * 50)
    
    # Get years from sidebar
    soup = fetch(BASE_URL)
    years = []
    if soup:
        for label in soup.find_all('a', href=re.compile(r'/search/label/')):
            m = re.search(r'/search/label/(\d{4})', label.get('href', ''))
            if m:
                year = int(m.group(1))
                if 1891 <= year <= 2019:
                    years.append(year)
        years = sorted(set(years))
    
    if not years:
        print("No years found!")
        return
    
    print(f"Found {len(years)} years to scrape: {years[0]}-{years[-1]}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print()
    
    total = 0
    completed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(scrape_single_year, year): year for year in years}
        
        for future in concurrent.futures.as_completed(futures):
            year = futures[future]
            try:
                _, matches = future.result()
                count = save_year_csv(year, matches)
                total += count
                completed += 1
                print(f"[{completed}/{len(years)}] Year {year}: {count} matches")
            except Exception as e:
                print(f"[{completed}/{len(years)}] Year {year}: ERROR - {e}")
    
    print()
    print("=" * 50)
    print(f"Complete! Total: {total} matches")

if __name__ == "__main__":
    main()
