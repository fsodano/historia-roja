#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import time

BASE_URL = "https://josecarluccio.blogspot.com/search/label/"
OUTPUT_DIR = "data"

def fetch(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_match(line):
    """Parse match line like '04/04/1936 en Avellaneda: Independiente 5, Barracas Central 1'"""
    pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+[^:]+:\s*([^,]+?)(\d+)\s*,\s*([^,]+?)(\d+)\s*$'
    m = re.search(pattern, line.strip())
    if not m:
        return None
    
    date = m.group(1)
    team1 = m.group(2).strip()
    score1 = m.group(3).strip()
    team2 = m.group(4).strip()
    score2 = m.group(5).strip()
    
    if 'independiente' not in team1.lower() and 'independiente' not in team2.lower():
        return None
    
    if 'independiente' in team1.lower():
        home, away = team1, team2
        hs, as_ = score1, score2
        result = "WIN" if int(hs) > int(as_) else "LOSS" if int(hs) < int(as_) else "DRAW"
    else:
        home, away = team1, team2
        hs, as_ = score1, score2
        result = "WIN" if int(as_) > int(hs) else "LOSS" if int(as_) < int(hs) else "DRAW"
    
    return {'date': date, 'home_team': home, 'away_team': away, 
            'home_score': hs, 'away_score': as_, 'result': result}

def get_competition(title):
    t = title.lower()
    if '1ra' in t or 'primera' in t:
        return '1ra. División'
    if '2da' in t:
        return '2da. División'
    if '3ra' in t:
        return '3ra. División'
    if 'copa' in t:
        return 'Copa'
    return 'Torneo'

def scrape_year(year):
    url = f"{BASE_URL}{year}"
    print(f"Scraping {year}...", end=" ", flush=True)
    
    soup = fetch(url)
    if not soup:
        print("FAILED")
        return []
    
    matches = []
    posts = soup.find_all('h3', class_='post-title')
    
    for post in posts:
        a = post.find('a')
        if not a or not a.get('href'):
            continue
        
        title = a.get_text(strip=True)
        comp = get_competition(title)
        
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
            m = parse_match(line)
            if m:
                m['competition'] = comp
                matches.append(m)
    
    print(f"found {len(matches)}")
    return matches

def save(year, matches):
    if not matches:
        return
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = os.path.join(OUTPUT_DIR, f"{year}.csv")
    
    existing = set()
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            r = csv.DictReader(f)
            for row in r:
                existing.add((row['date'], row['home_team'], row['away_team']))
    
    new = [m for m in matches if (m['date'], m['home_team'], m['away_team']) not in existing]
    
    if not new:
        return
    
    exists = os.path.exists(filename)
    with open(filename, 'a' if exists else 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        if not exists:
            w.writeheader()
        w.writerows(new)
    
    print(f"  Saved {len(new)} new")

def main():
    print("Scraping Independiente matches 1905-2019")
    total = 0
    
    for year in range(1905, 2020):
        matches = scrape_year(year)
        save(year, matches)
        total += len(matches)
        time.sleep(1)
    
    print(f"\nTotal matches: {total}")

if __name__ == "__main__":
    main()
