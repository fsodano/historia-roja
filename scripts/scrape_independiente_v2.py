#!/usr/bin/env python3
"""Scrape Independiente match data from josecarluccio.blogspot.com"""

import requests
from bs4 import BeautifulSoup
import re
import csv
import os

BASE_URL = "https://josecarluccio.blogspot.com/search/label/"
OUTPUT_DIR = "data"

def ensure_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def fetch_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"  Error: {e}")
        return None

def parse_match_line(line):
    """Parse a match line. Format: '04/04/1936 en Avellaneda: Independiente 5, Barracas Central 1'"""
    # Remove notes and extra whitespace
    line = re.sub(r'\*Nota:.*?\*', '', line)
    line = line.strip()
    
    # Match pattern: date en location: Team1 score1, Team2 score2
    pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^,]+?)(\d+)\s*,\s*([^\d]+?)(\d+)\s*$'
    
    match = re.search(pattern, line)
    if not match:
        return None
    
    date = match.group(1)
    location = match.group(2).strip()
    team1 = match.group(3).strip()
    score1 = match.group(4).strip()
    team2 = match.group(5).strip()
    score2 = match.group(6).strip()
    
    # Check if Independiente is in this match
    t1_lower = team1.lower()
    t2_lower = team2.lower()
    
    if 'independiente' not in t1_lower and 'independiente' not in t2_lower:
        return None
    
    # Determine home/away and result
    if 'independiente' in t1_lower:
        home_team, away_team = team1, team2
        home_score, away_score = score1, score2
        result = "WIN" if int(score1) > int(score2) else "LOSS" if int(score1) < int(score2) else "DRAW"
    else:
        home_team, away_team = team1, team2
        home_score, away_score = score1, score2
        result = "WIN" if int(score2) > int(score1) else "LOSS" if int(score2) < int(score1) else "DRAW"
    
    return {
        'date': date,
        'competition': '',
        'home_team': home_team,
        'away_team': away_team,
        'home_score': home_score,
        'away_score': away_score,
        'result': result
    }

def extract_competition(title, text):
    """Extract competition name"""
    title_lower = title.lower()
    
    patterns = [
        (r'1ra\.?\s*divisi', '1ra. División'),
        (r'2da\.?\s*divisi', '2da. División'),
        (r'3ra\.?\s*divisi', '3ra. División'),
        (r'copas?\s+interligas', 'Copas Interligas'),
        (r'copa\s+de\s+honor', 'Copa de Honor'),
        (r'copa\s+competencia', 'Copa Competencia'),
        (r'copa\s+ibarguren', 'Copa Ibarguren'),
        (r'copa\s+rosario|copa\s+culacciati', 'Copa Rosario'),
        (r'copa\s+mariano\s+reyna', 'Copa Mariano Reyna'),
        (r'campeonato\s+rioplatense', 'Campeonato Rioplatense'),
        (r'campeonato\s+argentino\s+interligas', 'Campeonato Argentino Interligas'),
        (r'torneo\s+preparación', 'Torneo Preparación'),
        (r'torneo\s+reducido', 'Torneo Reducido'),
        (r'copa\s+argentina', 'Copa Argentina'),
        (r'copa\s+libertadores', 'Copa Libertadores'),
        (r'copa\s+sudamericana', 'Copa Sudamericana'),
        (r'copa\s+de\s+la\s+liga', 'Copa de la Liga'),
        (r'supercopa', 'Supercopa'),
        (r'primera\s+b\s+nacional', 'Primera B Nacional'),
    ]
    
    for pattern, name in patterns:
        if re.search(pattern, title_lower):
            return name
    
    if any(x in title_lower for x in ['primera', 'liga', 'apertura', 'clausura', 'metropolitano', 'nacional']):
        return 'Primera División'
    
    return 'Torneo'

def scrape_year(year):
    """Scrape matches for a specific year"""
    url = f"{BASE_URL}{year}"
    print(f"Scraping {year}...", end=" ")
    
    soup = fetch_page(url)
    if not soup:
        print("FAILED")
        return []
    
    matches = []
    
    # Get all post links
    posts = soup.find_all('h3', class_='post-title')
    
    for post in posts:
        a_tag = post.find('a')
        if not a_tag or not a_tag.get('href'):
            continue
        
        title = a_tag.get_text(strip=True)
        post_url = a_tag['href']
        
        # Fetch post
        post_soup = fetch_page(post_url)
        if not post_soup:
            continue
        
        body = post_soup.find('div', class_='post-body')
        if not body:
            continue
        
        text = body.get_text()
        
        if 'independiente' not in text.lower():
            continue
        
        competition = extract_competition(title, text)
        
        # Find match lines
        lines = text.split('\n')
        for line in lines:
            match = parse_match_line(line)
            if match:
                match['competition'] = competition
                matches.append(match)
    
    print(f"found {len(matches)} matches")
    return matches

def save_csv(year, matches):
    """Save matches to CSV"""
    if not matches:
        return
    
    filename = os.path.join(OUTPUT_DIR, f"{year}.csv")
    
    # Read existing
    existing = set()
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.add((row['date'], row['home_team'], row['away_team']))
    
    # Filter new
    new_matches = [m for m in matches if (m['date'], m['home_team'], m['away_team']) not in existing]
    
    if not new_matches:
        return
    
    # Save
    file_exists = os.path.exists(filename)
    with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_matches)
    
    print(f"  Saved {len(new_matches)} new")

def main():
    ensure_dir()
    
    print("Independiente Match Scraper (1905-2019)")
    print("=" * 50)
    
    total = 0
    
    for year in range(1905, 2020):
        try:
            matches = scrape_year(year)
            save_csv(year, matches)
            total += len(matches)
        except Exception as e:
            print(f"  Error: {e}")
    
    print("=" * 50)
    print(f"Total: {total} matches")
    print(f"Files saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
