#!/usr/bin/env python3
"""Scrape Independiente matches with improved parsing"""

import requests
from bs4 import BeautifulSoup
import re
import csv

BASE_URL = "https://josecarluccio.blogspot.com/search/label/"
YEARS = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]

def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_post_links(soup):
    """Extract all post links from a label page"""
    links = []
    for post in soup.find_all('h3', class_='post-title'):
        a_tag = post.find('a')
        if a_tag and a_tag.get('href'):
            links.append(a_tag['href'])
    return links

def clean_team_name(name):
    """Clean team name - remove newlines and extra spaces"""
    name = name.replace('\n', ' ').replace('\r', ' ')
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

def is_independiente_avellaneda(name):
    """Check if team is Independiente from Avellaneda (not other Independiente teams)"""
    name_lower = name.lower()
    # Check if it's just "Independiente" without qualifiers like "de Chivilcoy", "de Chivilcoy", etc.
    if 'independiente' in name_lower:
        # Exclude other Independiente teams
        excluded = ['de chivilcoy', 'de bolivar', 'de dolores', 'de fernandez', 
                   'de general pico', 'de hipolito yrigoyen', 'de la rioja',
                   'de chivilcoy', 'fontana', 'de esteban']
        for ex in excluded:
            if ex in name_lower:
                return False
        return True
    return False

def extract_competition(title, text):
    """Extract competition name from title and text"""
    title_lower = title.lower()
    text_lower = text.lower()
    
    if 'copa libertadores' in title_lower:
        return 'Copa Libertadores'
    elif 'copa sudamericana' in title_lower:
        return 'Copa Sudamericana'
    elif 'copa argentina' in title_lower:
        return 'Copa Argentina'
    elif 'copa de la liga' in title_lower or 'copa de la superliga' in title_lower or 'copa superliga' in title_lower:
        return 'Copa de la Liga'
    elif 'supercopa' in title_lower:
        return 'Supercopa'
    elif 'primera nacional' in title_lower or 'primera b nacional' in title_lower:
        return 'Primera B Nacional'
    elif 'primera' in title_lower and ('division' in title_lower or 'afa' in title_lower):
        return 'Primera División'
    elif 'apertura' in title_lower or 'clausura' in title_lower or 'inicial' in title_lower or 'final' in title_lower:
        return 'Primera División'
    
    if 'copa libertadores' in text_lower:
        return 'Copa Libertadores'
    elif 'copa sudamericana' in text_lower:
        return 'Copa Sudamericana'
    elif 'primera nacional' in text_lower:
        return 'Primera B Nacional'
    
    return 'Primera División'

def extract_matches_from_text(text, competition):
    """Extract match data from text using regex patterns"""
    matches = []
    
    # Pattern with scorers: DD/MM/YYYY en [location]: [HomeTeam] [score] ([scorers]), [AwayTeam] [score]
    pattern1 = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d(]+?)\s+(\d+)\s*\([^)]*\)\s*,\s*([^\d(]+?)\s+(\d+)\s*$'
    
    # Pattern without scorers: DD/MM/YYYY en [location]: [HomeTeam] [score], [AwayTeam] [score]
    pattern2 = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d,]+?)\s+(\d+)\s*,\s*([^\d(]+?)\s+(\d+)\s*$'
    
    # Find all matches for pattern1
    for match in re.finditer(pattern1, text, re.IGNORECASE | re.MULTILINE):
        date = match.group(1)
        home_team = clean_team_name(match.group(3))
        home_score = match.group(4)
        away_team = clean_team_name(match.group(5))
        away_score = match.group(6)
        
        # Only include if Independiente (Avellaneda) is playing
        if is_independiente_avellaneda(home_team) or is_independiente_avellaneda(away_team):
            # Determine result from Independiente's perspective
            if is_independiente_avellaneda(home_team):
                if int(home_score) > int(away_score):
                    result = 'WIN'
                elif int(home_score) < int(away_score):
                    result = 'LOSS'
                else:
                    result = 'DRAW'
            else:
                if int(away_score) > int(home_score):
                    result = 'WIN'
                elif int(away_score) < int(home_score):
                    result = 'LOSS'
                else:
                    result = 'DRAW'
            
            matches.append({
                'date': date,
                'competition': competition,
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score,
                'result': result
            })
    
    # Find matches for pattern2 (without scorer info)
    for match in re.finditer(pattern2, text, re.IGNORECASE | re.MULTILINE):
        date = match.group(1)
        home_team = clean_team_name(match.group(3))
        home_score = match.group(4)
        away_team = clean_team_name(match.group(5))
        away_score = match.group(6)
        
        # Only include if Independiente (Avellaneda) is playing
        if is_independiente_avellaneda(home_team) or is_independiente_avellaneda(away_team):
            # Determine result from Independiente's perspective
            if is_independiente_avellaneda(home_team):
                if int(home_score) > int(away_score):
                    result = 'WIN'
                elif int(home_score) < int(away_score):
                    result = 'LOSS'
                else:
                    result = 'DRAW'
            else:
                if int(away_score) > int(home_score):
                    result = 'WIN'
                elif int(away_score) < int(home_score):
                    result = 'LOSS'
                else:
                    result = 'DRAW'
            
            matches.append({
                'date': date,
                'competition': competition,
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score,
                'result': result
            })
    
    return matches

def scrape_post(url, year):
    """Scrape a single post for Independiente matches"""
    soup = fetch_page(url)
    if not soup:
        return []
    
    # Get title
    title_tag = soup.find('h3', class_='post-title')
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    # Get text content
    text = soup.get_text()
    
    # Determine competition
    competition = extract_competition(title, text)
    
    # Extract matches
    matches = extract_matches_from_text(text, competition)
    
    return matches

def scrape_year(year):
    """Scrape all matches from a specific year"""
    url = f"{BASE_URL}{year}"
    print(f"\nScraping year {year}...")
    
    soup = fetch_page(url)
    if not soup:
        return []
    
    # Get all post links
    post_links = extract_post_links(soup)
    print(f"Found {len(post_links)} posts")
    
    all_matches = []
    for link in post_links:
        matches = scrape_post(link, year)
        all_matches.extend(matches)
        if matches:
            print(f"  Found {len(matches)} matches in: {link}")
    
    return all_matches

def main():
    all_matches = []
    
    for year in YEARS:
        matches = scrape_year(year)
        all_matches.extend(matches)
        print(f"Year {year}: {len(matches)} matches found")
    
    # Remove duplicates
    seen = set()
    unique_matches = []
    for match in all_matches:
        key = (match['date'], match['home_team'], match['away_team'])
        if key not in seen:
            seen.add(key)
            unique_matches.append(match)
    
    # Sort by date
    unique_matches.sort(key=lambda x: x['date'])
    
    # Write to CSV
    with open('independiente_matches.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        writer.writeheader()
        writer.writerows(unique_matches)
    
    print(f"\n{'='*60}")
    print(f"Total unique matches found: {len(unique_matches)}")
    print("Data saved to independiente_matches.csv")

if __name__ == "__main__":
    main()
