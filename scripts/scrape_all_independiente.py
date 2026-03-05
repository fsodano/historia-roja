#!/usr/bin/env python3
"""Comprehensive scraper for Independiente matches from josecarluccio.blogspot.com"""

import requests
from bs4 import BeautifulSoup
import re
import csv
import time

BASE_URL = "https://josecarluccio.blogspot.com"
YEARS = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]

def fetch_page(url, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"  Retry {attempt+1}/{max_retries} for {url}: {e}")
            time.sleep(2)
    return None

def get_all_posts_for_year(year):
    """Get all post links for a year with pagination"""
    all_links = []
    url = f"{BASE_URL}/search/label/{year}"
    page_count = 0
    
    while url and page_count < 10:  # Limit to 10 pages
        page_count += 1
        soup = fetch_page(url)
        if not soup:
            break
        
        # Extract post links
        for post in soup.find_all('h3', class_='post-title'):
            a_tag = post.find('a')
            if a_tag and a_tag.get('href'):
                href = a_tag['href']
                if href not in all_links:
                    all_links.append(href)
        
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
    name = name.strip()
    # Remove HTML entities
    name = name.replace('&#8217;', "'").replace('&#8220;', '"').replace('&#8221;', '"')
    name = name.replace('&nbsp;', ' ')
    return name.strip()

def is_independiente_avellaneda(name):
    """Check if team is Independiente from Avellaneda"""
    name_lower = name.lower().strip()
    if 'independiente' not in name_lower:
        return False
    # Exclude other Independiente teams
    excluded = [
        'de chivilcoy', 'de bolivar', 'de dolores', 'de fernandez', 
        'de general pico', 'de hipolito yrigoyen', 'de la rioja',
        'fontana', 'de esteban', 'chivilcoy', 'de chivilcoy',
        'de bolívar', 'de fernández', 'de chivilcoy'
    ]
    for ex in excluded:
        if ex in name_lower:
            return False
    return True

def extract_competition(title):
    """Extract competition name from title"""
    title_lower = title.lower()
    
    if 'copa libertadores' in title_lower:
        return 'Copa Libertadores'
    elif 'copa sudamericana' in title_lower:
        return 'Copa Sudamericana'
    elif 'copa argentina' in title_lower:
        return 'Copa Argentina'
    elif 'supercopa' in title_lower:
        return 'Supercopa'
    elif 'primera b nacional' in title_lower or 'primera nacional' in title_lower or '1ra b nacional' in title_lower:
        return 'Primera B Nacional'
    elif 'torneo inicial' in title_lower:
        return 'Torneo Inicial'
    elif 'torneo final' in title_lower:
        return 'Torneo Final'
    elif 'torneo apertura' in title_lower:
        return 'Torneo Apertura'
    elif 'torneo clausura' in title_lower:
        return 'Torneo Clausura'
    elif 'primera division' in title_lower or '1ra division' in title_lower or 'primera' in title_lower:
        return 'Primera División'
    else:
        return 'Primera División'

def extract_year_from_date(date_str):
    """Extract year from date string DD/MM/YYYY"""
    try:
        return int(date_str.split('/')[-1])
    except:
        return None

def extract_matches_from_text(text, competition, post_url):
    """Extract match data from text"""
    matches = []
    
    # Clean text
    text = text.replace('&#8217;', "'").replace('&#8220;', '"').replace('&#8221;', '"')
    text = text.replace('&nbsp;', ' ')
    
    # Pattern 1: DD/MM/YYYY en [location]: [HomeTeam] [score] ([scorers]), [AwayTeam] [score]
    # Example: 07/09/2011 en Avellaneda: Independiente 2 (Marco Pérez 2), San Martín de San Juan 1
    pattern1 = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d(]+?)\s+(\d+)\s*\([^)]*\)\s*,\s*([^\d(]+?)\s+(\d+)(?:\s|$)'
    
    # Pattern 2: DD/MM/YYYY en [location]: [HomeTeam] [score], [AwayTeam] [score]
    # Example: 07/09/2011 en Avellaneda: Independiente 2, San Martín de San Juan 1
    pattern2 = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d,]+?)\s+(\d+)\s*,\s*([^\d(]+?)\s+(\d+)(?:\s|$)'
    
    for pattern in [pattern1, pattern2]:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            try:
                date = match.group(1)
                home_team = clean_team_name(match.group(3))
                home_score = match.group(4)
                away_team = clean_team_name(match.group(5))
                away_score = match.group(6)
                
                # Skip if no scores
                if not home_score or not away_score:
                    continue
                
                # Check if Independiente (Avellaneda) is playing
                home_is_ind = is_independiente_avellaneda(home_team)
                away_is_ind = is_independiente_avellaneda(away_team)
                
                if home_is_ind or away_is_ind:
                    # Determine result from Independiente's perspective
                    try:
                        h_score = int(home_score)
                        a_score = int(away_score)
                        
                        if home_is_ind:
                            if h_score > a_score:
                                result = 'WIN'
                            elif h_score < a_score:
                                result = 'LOSS'
                            else:
                                result = 'DRAW'
                        else:
                            if a_score > h_score:
                                result = 'WIN'
                            elif a_score < h_score:
                                result = 'LOSS'
                            else:
                                result = 'DRAW'
                        
                        matches.append({
                            'date': date,
                            'competition': competition,
                            'home_team': home_team,
                            'away_team': away_team,
                            'home_score': str(h_score),
                            'away_score': str(a_score),
                            'result': result
                        })
                    except ValueError:
                        continue
            except Exception as e:
                continue
    
    return matches

def scrape_post(url):
    """Scrape a single post for matches"""
    soup = fetch_page(url)
    if not soup:
        return []
    
    title_tag = soup.find('h3', class_='post-title')
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    # Get text content
    text = soup.get_text()
    
    competition = extract_competition(title)
    matches = extract_matches_from_text(text, competition, url)
    
    return matches

def main():
    all_matches = []
    
    for year in YEARS:
        print(f"\n{'='*60}")
        print(f"Year {year}")
        print('='*60)
        
        post_links = get_all_posts_for_year(year)
        print(f"Found {len(post_links)} posts")
        
        year_matches = []
        for i, link in enumerate(post_links):
            print(f"  [{i+1}/{len(post_links)}] {link}")
            matches = scrape_post(link)
            if matches:
                # Filter matches for the current year
                for match in matches:
                    match_year = extract_year_from_date(match['date'])
                    if match_year and str(match_year) == year:
                        year_matches.append(match)
                        print(f"    + Match: {match['date']} - {match['home_team']} {match['home_score']}-{match['away_score']} {match['away_team']}")
        
        print(f"Year {year}: {len(year_matches)} matches")
        all_matches.extend(year_matches)
    
    # Remove duplicates
    seen = set()
    unique_matches = []
    for match in all_matches:
        key = (match['date'], match['home_team'], match['away_team'], match['home_score'], match['away_score'])
        if key not in seen:
            seen.add(key)
            unique_matches.append(match)
    
    # Sort by date
    unique_matches.sort(key=lambda x: (x['date'].split('/')[-1], x['date'].split('/')[1], x['date'].split('/')[0]))
    
    # Write to CSV
    output_file = 'independiente_matches_all.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        writer.writeheader()
        writer.writerows(unique_matches)
    
    print(f"\n{'='*60}")
    print(f"Total unique matches: {len(unique_matches)}")
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
