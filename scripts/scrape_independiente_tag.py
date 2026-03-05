#!/usr/bin/env python3
"""
Scrape Independiente matches from the 'independiente' tag pages
Iterates through all pages and extracts match data
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
    Parse match line with format: date en location: Team1 X (scorers), Team2 Y (scorers)
    Example: 06/12/2017 en Avellaneda: Independiente de Argentina 2 (Emanuel Gigliotti y Maximiliano Meza), Flamengo de Brasil 1 (Réver)
    """
    line = line.strip()
    if not line:
        return None
    
    # Pattern: DD/MM/YYYY en location: Team1 score1, Team2 score2
    # The pattern should stop at the first digit of the score, ignoring any text in parentheses
    pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d(][^\d,]*?)(\d+)\s*(?:\([^)]*\))?\s*,\s*([^\d(][^\d,]*?)(\d+)\s*(?:\([^)]*\))?\s*$'
    m = re.search(pattern, line)
    
    if not m:
        return None
    
    date, location, team1, score1, team2, score2 = m.groups()
    team1 = team1.strip()
    team2 = team2.strip()
    
    # Check if Independiente (de Avellaneda/Argentina) is in this match
    t1_lower = team1.lower()
    t2_lower = team2.lower()
    
    # Filter for Independiente de Avellaneda/Argentina specifically
    is_inde1 = 'independiente' in t1_lower
    is_inde2 = 'independiente' in t2_lower
    
    # Exclude Independiente Santa Fe (Colombia) unless explicitly requested
    if 'santa fe' in t1_lower or 'colombia' in t1_lower:
        is_inde1 = False
    if 'santa fe' in t2_lower or 'colombia' in t2_lower:
        is_inde2 = False
    
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

def extract_competition(title, text_content=""):
    """Extract competition name from post title"""
    t = title.lower()
    
    # Copa Sudamericana
    if 'copa sudamericana' in t:
        year_match = re.search(r'\b(20\d{2})\b', t)
        if year_match:
            return f"Copa Sudamericana {year_match.group(1)}"
        return "Copa Sudamericana"
    
    # Copa Libertadores
    if 'copa libertadores' in t:
        year_match = re.search(r'\b(20\d{2})\b', t)
        if year_match:
            return f"Copa Libertadores {year_match.group(1)}"
        return "Copa Libertadores"
    
    # Copa Argentina
    if 'copa argentina' in t:
        return "Copa Argentina"
    
    # Copa Competencia, Copa de Honor, etc.
    if 'copa competencia' in t:
        return "Copa Competencia"
    if 'copa de honor' in t:
        return "Copa de Honor"
    if 'copa ibarguren' in t:
        return "Copa Ibarguren"
    
    # Division competitions
    if 'primera b nacional' in t or '1ra. "b" nacional' in t:
        year_match = re.search(r'\b(20\d{2})\b', t)
        if year_match:
            return f"Primera B Nacional {year_match.group(1)}"
        return "Primera B Nacional"
    
    if '1ra' in t or 'primera división' in t or 'primera division' in t:
        year_match = re.search(r'\b(20\d{2})\b', t)
        if year_match:
            return f"Primera División {year_match.group(1)}"
        return "Primera División"
    
    if '2da' in t or 'segunda división' in t:
        return "2da. División"
    
    # Torneo Apertura/Clausura
    if 'torneo apertura' in t or 'apertura' in t:
        year_match = re.search(r'\b(20\d{2})\b', t)
        if year_match:
            return f"Torneo Apertura {year_match.group(1)}"
        return "Torneo Apertura"
    
    if 'torneo clausura' in t or 'clausura' in t:
        year_match = re.search(r'\b(20\d{2})\b', t)
        if year_match:
            return f"Torneo Clausura {year_match.group(1)}"
        return "Torneo Clausura"
    
    # Metropolitano/Nacional
    if 'metropolitano' in t:
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', t)
        if year_match:
            return f"Metropolitano {year_match.group(1)}"
        return "Metropolitano"
    
    if 'nacional' in t:
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', t)
        if year_match:
            return f"Nacional {year_match.group(1)}"
        return "Nacional"
    
    # Extract year from text content as fallback
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', title)
    if year_match:
        return f"Torneo {year_match.group(1)}"
    
    return "Torneo"

def get_year_from_date(date_str):
    """Extract year from date string DD/MM/YYYY"""
    try:
        return date_str.split('/')[-1]
    except:
        return None

def scrape_post(post_url, title):
    """Scrape a single post and extract match data"""
    soup = fetch(post_url)
    if not soup:
        return []
    
    matches = []
    competition = extract_competition(title)
    
    # Get post body
    body = soup.find('div', class_='post-body')
    if not body:
        return matches
    
    text = body.get_text()
    
    # Parse each line
    for line in text.split('\n'):
        match = parse_match_line(line, competition)
        if match:
            matches.append(match)
    
    return matches

def scrape_independiente_pages():
    """Scrape all pages of the independiente tag"""
    all_matches = []
    page_num = 1
    
    # Start with first page
    current_url = f"{BASE_URL}/search/label/independiente"
    
    print("Scraping Independiente tag pages...")
    print("=" * 60)
    
    while current_url and page_num <= 20:  # Limit to 20 pages to avoid infinite loops
        print(f"\nPage {page_num}: {current_url}")
        
        soup = fetch(current_url)
        if not soup:
            print("  Failed to fetch page")
            break
        
        # Find all post titles
        posts = soup.find_all('h3', class_='post-title')
        print(f"  Found {len(posts)} posts")
        
        for post in posts:
            a_tag = post.find('a')
            if not a_tag or not a_tag.get('href'):
                continue
            
            title = a_tag.get_text(strip=True)
            post_url = urljoin(BASE_URL, a_tag['href'])
            
            print(f"    Processing: {title[:60]}...")
            
            # Scrape the post
            matches = scrape_post(post_url, title)
            print(f"      Found {len(matches)} matches")
            
            all_matches.extend(matches)
        
        # Find next page link
        next_link = None
        for a in soup.find_all('a'):
            if a.get_text(strip=True) == 'Entradas antiguas' or 'older' in a.get('href', '').lower():
                next_link = urljoin(BASE_URL, a['href'])
                break
        
        if not next_link or next_link == current_url:
            break
        
        current_url = next_link
        page_num += 1
        time.sleep(1)  # Be polite
    
    return all_matches

def save_matches_by_year(matches):
    """Save matches to CSV files organized by year"""
    if not matches:
        print("\nNo matches to save!")
        return
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Group matches by year
    matches_by_year = {}
    for m in matches:
        year = get_year_from_date(m['date'])
        if year:
            if year not in matches_by_year:
                matches_by_year[year] = []
            matches_by_year[year].append(m)
    
    total_saved = 0
    
    for year, year_matches in sorted(matches_by_year.items()):
        filename = os.path.join(DATA_DIR, f"{year}.csv")
        
        # Remove duplicates
        seen = set()
        unique = []
        for m in year_matches:
            key = (m['date'], m['home_team'], m['away_team'])
            if key not in seen:
                seen.add(key)
                unique.append(m)
        
        # Append or create new file
        file_exists = os.path.exists(filename)
        
        with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
            if not file_exists:
                writer.writeheader()
            writer.writerows(unique)
        
        print(f"  {year}: {len(unique)} matches -> {filename}")
        total_saved += len(unique)
    
    return total_saved

def main():
    print("=" * 60)
    print("Independiente Match Scraper (via 'independiente' tag)")
    print("=" * 60)
    print()
    
    # Scrape all pages
    matches = scrape_independiente_pages()
    
    print("\n" + "=" * 60)
    print(f"Total matches extracted: {len(matches)}")
    print("=" * 60)
    
    # Save by year
    if matches:
        print("\nSaving matches to CSV files...")
        total_saved = save_matches_by_year(matches)
        print(f"\nTotal saved: {total_saved} matches")
        print(f"Files saved to: {DATA_DIR}/")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
