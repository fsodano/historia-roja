#!/usr/bin/env python3
"""Final scraper for Independiente de Avellaneda matches only"""

import requests
from bs4 import BeautifulSoup
import re
import csv

# URLs for Independiente-specific posts
INDEPENDIENTE_URLS = [
    # 2011 - Torneo Apertura 2011
    "https://josecarluccio.blogspot.com/2015/06/argentina-1ra-division-afa-torneo.html",
    # 2012 - Torneo Inicial 2012
    "https://josecarluccio.blogspot.com/2016/01/argentina-1ra-division-afa-torneo.html",
    # 2012 - Torneo Final 2013 (Clausura 2012 matches)
    "https://josecarluccio.blogspot.com/2016/01/argentina-1ra-division-afa-torneo_10.html",
    # 2013 - Primera B Nacional 2013/14
    "https://josecarluccio.blogspot.com/2016/07/argentina-1ra-b-nacional-afa-2013-14.html",
    # 2014 - Torneo de Transición 2014
    "https://josecarluccio.blogspot.com/2017/03/argentina-1ra-d-afa-torneo-de_11.html",
    # 2014 - Primera Nacional 2014
    "https://josecarluccio.blogspot.com/2017/03/argentina-1ra-d-afa-torneo-de_8.html",
    # 2015 - Torneo 2015
    "https://josecarluccio.blogspot.com/2017/08/argentina-1ra-d-afa-2015-torneo.html",
    # 2016 - Primera División 2016
    "https://josecarluccio.blogspot.com/2017/12/argentina-1ra-d-afa-2016-torneo.html",
    # 2017 - Copa Sudamericana 2017
    "https://josecarluccio.blogspot.com/2020/12/copa-sudamericana-2017-final.html",
    # 2017 - Primera División 2016/17
    "https://josecarluccio.blogspot.com/2017/12/argentina-1ra-d-afa-2016-torneo.html",
    # 2018 - Supercopa Argentina 2018
    "https://josecarluccio.blogspot.com/2025/11/argentina-supercopa-argentina-2018.html",
]

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

def clean_team_name(name):
    """Clean team name"""
    name = name.replace('\n', ' ').replace('\r', ' ')
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

def is_independiente_avellaneda(name):
    """Check if team is Independiente from Avellaneda only"""
    name_lower = name.lower().strip()
    if 'independiente' not in name_lower:
        return False
    # Exclude other Independiente teams
    excluded = [
        'de chivilcoy', 'de bolivar', 'de bolívar', 'de dolores', 'de fernandez', 
        'de fernández', 'de general pico', 'de hipolito yrigoyen', 'de la rioja',
        'fontana', 'de esteban', 'chivilcoy', 'de coronel', 'de mones',
        'de neuquén', 'de neuquen', 'de río colorado', 'de rio colorado',
        'de tandil', 'fc de américa', 'atlético', 'atl&#233;tico'
    ]
    for ex in excluded:
        if ex in name_lower:
            return False
    return True

def extract_competition_from_title(title):
    """Extract competition from title"""
    title_lower = title.lower()
    
    if 'copa sudamericana' in title_lower:
        return 'Copa Sudamericana'
    elif 'copa libertadores' in title_lower:
        return 'Copa Libertadores'
    elif 'copa argentina' in title_lower:
        return 'Copa Argentina'
    elif 'supercopa' in title_lower:
        return 'Supercopa Argentina'
    elif 'primera b nacional' in title_lower or '1ra b nacional' in title_lower:
        return 'Primera B Nacional'
    elif 'torneo apertura' in title_lower:
        return 'Torneo Apertura'
    elif 'torneo clausura' in title_lower:
        return 'Torneo Clausura'
    elif 'torneo inicial' in title_lower:
        return 'Torneo Inicial'
    elif 'torneo final' in title_lower:
        return 'Torneo Final'
    elif 'torneo de transicion' in title_lower or 'torneo de transición' in title_lower:
        return 'Torneo de Transición'
    elif 'primera division' in title_lower or '1ra division' in title_lower:
        return 'Primera División'
    else:
        return 'Primera División'

def extract_matches_from_text(text, competition):
    """Extract match data"""
    matches = []
    
    # Clean text
    text = text.replace('\u0026#8217;', "'").replace('\u0026#8220;', '"').replace('\u0026#8221;', '"')
    text = text.replace('\u0026#233;', 'e')
    
    # Pattern with scorers: DD/MM/YYYY en [location]: [Home] [score] ([scorers]), [Away] [score]
    pattern1 = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d(]+?)\s+(\d+)\s*\([^)]*\)\s*,\s*([^\d(]+?)\s+(\d+)(?:\s|$)'
    
    # Pattern without scorers: DD/MM/YYYY en [location]: [Home] [score], [Away] [score]
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
                
                # Check if Independiente Avellaneda is playing
                home_is_ind = is_independiente_avellaneda(home_team)
                away_is_ind = is_independiente_avellaneda(away_team)
                
                if home_is_ind or away_is_ind:
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
            except Exception:
                continue
    
    return matches

def scrape_post(url):
    """Scrape a post"""
    soup = fetch_page(url)
    if not soup:
        return []
    
    title_tag = soup.find('h3', class_='post-title')
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    text = soup.get_text()
    competition = extract_competition_from_title(title)
    matches = extract_matches_from_text(text, competition)
    
    return matches, title

def main():
    all_matches = []
    
    for url in INDEPENDIENTE_URLS:
        print(f"\nScraping: {url}")
        matches, title = scrape_post(url)
        print(f"  Title: {title[:60]}...")
        print(f"  Found {len(matches)} matches")
        all_matches.extend(matches)
    
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
    output_file = 'independiente_matches_final.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        writer.writeheader()
        writer.writerows(unique_matches)
    
    print(f"\n{'='*60}")
    print(f"Total matches: {len(unique_matches)}")
    print(f"Data saved to {output_file}")
    
    # Print all matches
    print("\n=== ALL MATCHES ===")
    for m in unique_matches:
        print(f"{m['date']},{m['competition']},{m['home_team']},{m['away_team']},{m['home_score']},{m['away_score']},{m['result']}")

if __name__ == "__main__":
    main()
