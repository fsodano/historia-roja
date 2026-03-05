#!/usr/bin/env python3
"""
Proper scraper for ALL Independiente matches from josecarluccio.blogspot.com
Iterates through all year labels (1891-2019) and extracts match data
"""

import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import time
from urllib.parse import urljoin

BASE_URL = "https://josecarluccio.blogspot.com"
DATA_DIR = "data"

def fetch(url):
    """Fetch a URL and return BeautifulSoup object"""
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None

def parse_match_line(line, competition=""):
    """
    Parse match line. Handles formats:
    - "04/04/1936 en Avellaneda: Independiente 5, Barracas Central 1"
    - "06/12/2017 en Avellaneda: Independiente de Argentina 2 (Emanuel Gigliotti...), Flamengo 1"
    """
    line = line.strip()
    if not line:
        return None
    
    # Pattern: DD/MM/YYYY en location: Team1 X, Team2 Y
    # Stop at first number for score, ignore anything in parentheses after
    pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d(]+?)(\d+)\s*(?:\([^)]*\))?\s*,\s*([^\d(]+?)(\d+)\s*(?:\([^)]*\))?\s*$'
    m = re.search(pattern, line)
    
    if not m:
        return None
    
    date, location, team1, score1, team2, score2 = m.groups()
    team1 = team1.strip()
    team2 = team2.strip()
    
    # Check if Independiente is in this match (but NOT Independiente Santa Fe)
    t1_lower = team1.lower()
    t2_lower = team2.lower()
    
    is_inde1 = 'independiente' in t1_lower and 'santa fe' not in t1_lower
    is_inde2 = 'independiente' in t2_lower and 'santa fe' not in t2_lower
    
    if not is_inde1 and not is_inde2:
        return None
    
    # Determine home/away and result from Independiente's perspective
    try:
        s1, s2 = int(score1), int(score2)
        if is_inde1:  # Independiente is home team
            home_team, away_team = team1, team2
            home_score, away_score = score1, score2
            result = "WIN" if s1 > s2 else "LOSS" if s1 < s2 else "DRAW"
        else:  # Independiente is away team
            home_team, away_team = team1, team2
            home_score, away_score = score1, score2
            result = "WIN" if s2 > s1 else "LOSS" if s2 < s1 else "DRAW"
    except:
        return None
    
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
    
    # Extract year first
    year_match = re.search(r'\b(\d{4})\b', title)
    year = year_match.group(1) if year_match else ""
    
    if 'copa sudamericana' in t:
        return f"Copa Sudamericana {year}" if year else "Copa Sudamericana"
    elif 'copa libertadores' in t:
        return f"Copa Libertadores {year}" if year else "Copa Libertadores"
    elif 'copa argentina' in t:
        return "Copa Argentina"
    elif 'copa de honor' in t:
        return "Copa de Honor"
    elif 'copa competencia' in t:
        return "Copa Competencia"
    elif 'copa ibarguren' in t:
        return "Copa Ibarguren"
    elif 'copas interligas' in t:
        return "Copas Interligas"
    elif 'primera b nacional' in t:
        return f"Primera B Nacional {year}" if year else "Primera B Nacional"
    elif '2da' in t or 'segunda division' in t:
        return f"2da. División {year}" if year else "2da. División"
    elif 'metropolitano' in t:
        return f"Metropolitano {year}" if year else "Metropolitano"
    elif 'nacional' in t:
        return f"Nacional {year}" if year else "Nacional"
    elif 'apertura' in t:
        return f"Torneo Apertura {year}" if year else "Torneo Apertura"
    elif 'clausura' in t:
        return f"Torneo Clausura {year}" if year else "Torneo Clausura"
    elif '1ra' in t or 'primera division' in t:
        return f"1ra. División {year}" if year else "1ra. División"
    elif 'campeonato' in t:
        return f"Campeonato {year}" if year else "Campeonato"
    elif 'torneo' in t:
        return f"Torneo {year}" if year else "Torneo"
    
    return f"Torneo {year}" if year else "Torneo"

def scrape_year(year):
    """Scrape all Independiente matches for a specific year"""
    url = f"{BASE_URL}/search/label/{year}"
    soup = fetch(url)
    
    if not soup:
        return []
    
    matches = []
    
    # Find all post titles on the year page
    posts = soup.find_all('h3', class_='post-title')
    
    for post in posts:
        a = post.find('a')
        if not a or not a.get('href'):
            continue
        
        title = a.get_text(strip=True)
        post_url = urljoin(BASE_URL, a['href'])
        
        # Extract competition from title
        competition = extract_competition(title)
        
        # Fetch the post content
        post_soup = fetch(post_url)
        if not post_soup:
            continue
        
        # Look for post body
        body = post_soup.find('div', class_='post-body')
        if not body:
            # Try alternative selectors
            body = post_soup.find('div', class_='entry-content') or post_soup.find('article')
        
        if not body:
            continue
        
        text = body.get_text()
        
        # Check if Independiente is mentioned
        if 'independiente' not in text.lower():
            continue
        
        # Parse each line for match data
        found_matches = 0
        for line in text.split('\n'):
            match = parse_match_line(line, competition)
            if match:
                matches.append(match)
                found_matches += 1
        
        if found_matches > 0:
            print(f"    {title[:60]}: {found_matches} matches")
    
    return matches

def save_year_csv(year, matches):
    """Save matches to CSV file for the year"""
    if not matches:
        return 0
    
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = os.path.join(DATA_DIR, f"{year}.csv")
    
    # Remove duplicates
    seen = set()
    unique = []
    for m in matches:
        key = (m['date'], m['home_team'], m['away_team'])
        if key not in seen:
            seen.add(key)
            unique.append(m)
    
    # Write to CSV
    file_exists = os.path.exists(filename)
    with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        if not file_exists:
            w.writeheader()
        w.writerows(unique)
    
    return len(unique)

def main():
    # Scrape years 1891-2019
    years = list(range(1891, 2020))
    total = 0
    
    print("="*60)
    print("Independiente Match Scraper - ALL YEARS (1891-2019)")
    print("="*60)
    print()
    
    for i, year in enumerate(years, 1):
        print(f"[{i}/{len(years)}] Year {year}...", end=" ", flush=True)
        matches = scrape_year(year)
        count = save_year_csv(year, matches)
        print(f"found {len(matches)}, saved {count}")
        total += count
        
        # Be polite - wait between years
        time.sleep(1)
    
    print()
    print("="*60)
    print(f"COMPLETE! Total: {total} matches")
    print("="*60)

if __name__ == "__main__":
    main()
