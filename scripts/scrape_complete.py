#!/usr/bin/env python3
"""Scrape Independiente matches with complete parsing"""

import requests
from bs4 import BeautifulSoup
import re
import csv
from urllib.parse import urljoin

BASE_URL = "https://josecarluccio.blogspot.com"
YEARS = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]

def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_all_posts_for_year(year):
    """Get all post links for a year, including pagination"""
    all_links = []
    url = f"{BASE_URL}/search/label/{year}"
    
    while url:
        print(f"  Fetching: {url}")
        soup = fetch_page(url)
        if not soup:
            break
        
        # Extract post links
        for post in soup.find_all('h3', class_='post-title'):
            a_tag = post.find('a')
            if a_tag and a_tag.get('href'):
                all_links.append(a_tag['href'])
        
        # Find next page link
        next_link = soup.find('a', class_='blog-pager-older-link')
        if next_link and next_link.get('href'):
            url = next_link['href']
        else:
            url = None
    
    return all_links

def clean_team_name(name):
    """Clean team name"""
    name = name.replace('\n', ' ').replace('\r', ' ')
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

def is_independiente_avellaneda(name):
    """Check if team is Independiente from Avellaneda"""
    name_lower = name.lower().strip()
    if 'independiente' in name_lower:
        excluded = ['de chivilcoy', 'de bolivar', 'de dolores', 'de fernandez', 
                   'de general pico', 'de hipolito yrigoyen', 'de la rioja',
                   'fontana', 'de esteban', 'de chivilcoy', 'chivilcoy']
        for ex in excluded:
            if ex in name_lower:
                return False
        return True
    return False

def extract_competition(title, text):
    """Extract competition name"""
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
    
    return 'Primera División'

def extract_matches_from_text(text, competition):
    """Extract match data from text"""
    matches = []
    
    # Pattern with scorers in parentheses
    pattern1 = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d(]+?)\s+(\d+)\s*\([^)]*\)\s*,\s*([^\d(]+?)\s+(\d+)\s*$'
    
    # Pattern without scorers
    pattern2 = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d,]+?)\s+(\d+)\s*,\s*([^\d(]+?)\s+(\d+)\s*$'
    
    for pattern in [pattern1, pattern2]:
        for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
            date = match.group(1)
            home_team = clean_team_name(match.group(3))
            home_score = match.group(4)
            away_team = clean_team_name(match.group(5))
            away_score = match.group(6)
            
            # Check for Independiente (Avellaneda)
            home_is_ind = is_independiente_avellaneda(home_team)
            away_is_ind = is_independiente_avellaneda(away_team)
            
            if home_is_ind or away_is_ind:
                # Determine result
                if home_is_ind:
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

def scrape_post(url):
    """Scrape a single post"""
    soup = fetch_page(url)
    if not soup:
        return []
    
    title_tag = soup.find('h3', class_='post-title')
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    text = soup.get_text()
    competition = extract_competition(title, text)
    matches = extract_matches_from_text(text, competition)
    
    return matches

def main():
    all_matches = []
    
    for year in YEARS:
        print(f"\n{'='*60}")
        print(f"Scraping year {year}...")
        print('='*60)
        
        post_links = get_all_posts_for_year(year)
        print(f"Found {len(post_links)} total posts")
        
        year_matches = []
        for i, link in enumerate(post_links):
            matches = scrape_post(link)
            if matches:
                print(f"  [{i+1}/{len(post_links)}] Found {len(matches)} matches in post")
                year_matches.extend(matches)
        
        print(f"Year {year}: {len(year_matches)} total matches")
        all_matches.extend(year_matches)
    
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
