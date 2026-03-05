#!/usr/bin/env python3
"""Complete scraper for Independiente de Avellaneda matches 2011-2019"""

import requests
from bs4 import BeautifulSoup
import re
import csv

# Known URLs for Independiente matches 2011-2019
URLS = {
    "2011": [
        ("https://josecarluccio.blogspot.com/2015/06/argentina-1ra-division-afa-torneo.html", "Torneo Apertura 2011"),
    ],
    "2012": [
        ("https://josecarluccio.blogspot.com/2016/01/argentina-1ra-division-afa-torneo.html", "Torneo Inicial 2012"),
        ("https://josecarluccio.blogspot.com/2016/01/argentina-1ra-division-afa-torneo_10.html", "Torneo Final 2013"),  # Clausura 2012 matches
    ],
    "2013": [
        ("https://josecarluccio.blogspot.com/2016/07/argentina-1ra-b-nacional-afa-2013-14.html", "Primera B Nacional 2013/14"),
    ],
    "2014": [
        ("https://josecarluccio.blogspot.com/2017/03/argentina-1ra-d-afa-torneo-de.html", "Torneo Final 2014"),  # Independiente back in Primera
        ("https://josecarluccio.blogspot.com/2017/08/argentina-1ra-d-afa-2015.html", "Primera División 2014"),
    ],
    "2015": [
        ("https://josecarluccio.blogspot.com/2017/08/argentina-1ra-d-afa-2015-torneo.html", "Primera División 2015"),
        ("https://josecarluccio.blogspot.com/2025/10/supercopa-argentina-2015.html", "Supercopa Argentina 2015"),
    ],
    "2016": [
        ("https://josecarluccio.blogspot.com/2017/12/argentina-1ra-d-afa-2016-torneo.html", "Primera División 2016"),
        ("https://josecarluccio.blogspot.com/2018/04/copa-libertadores-2016.html", "Copa Libertadores 2016"),
    ],
    "2017": [
        ("https://josecarluccio.blogspot.com/2018/04/argentina-1ra-d-sa-2016-17.html", "Primera División 2016/17"),
        ("https://josecarluccio.blogspot.com/2020/12/copa-sudamericana-2017-final.html", "Copa Sudamericana 2017"),
    ],
    "2018": [
        ("https://josecarluccio.blogspot.com/2019/07/argentina-superliga-2017-18.html", "Superliga 2017/18"),
        ("https://josecarluccio.blogspot.com/2025/11/argentina-supercopa-argentina-2018.html", "Supercopa Argentina 2018"),
        ("https://josecarluccio.blogspot.com/2022/02/copa-libertadores-2018.html", "Copa Libertadores 2018"),
    ],
    "2019": [
        ("https://josecarluccio.blogspot.com/2020/02/argentina-superliga-2018-19.html", "Superliga 2018/19"),
        ("https://josecarluccio.blogspot.com/2020/02/copa-de-la-superliga-2019.html", "Copa de la Superliga 2019"),
        ("https://josecarluccio.blogspot.com/2022/03/copa-sudamericana-2019.html", "Copa Sudamericana 2019"),
    ],
}

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
    name = name.replace('\n', ' ').replace('\r', ' ')
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

def is_independiente_avellaneda(name):
    name_lower = name.lower().strip()
    if 'independiente' not in name_lower:
        return False
    # Only exclude clearly different teams
    excluded = ['de chivilcoy', 'de bolivar', 'de bolívar', 'de dolores', 
                'de fernandez', 'de fernández', 'de general pico', 
                'de hipolito yrigoyen', 'de la rioja', 'fontana', 
                'de esteban', 'de chivilcoy', 'de neuquén', 'de neuquen',
                'de río colorado', 'de rio colorado', 'de tandil',
                'de coronel', 'de mones', 'fc de américa', 'atlético']
    for ex in excluded:
        if ex in name_lower:
            return False
    return True

def extract_matches_from_text(text, default_competition):
    matches = []
    
    # Clean text
    text = text.replace('\u0026#8217;', "'").replace('\u0026#8220;', '"').replace('\u0026#8221;', '"')
    text = text.replace('\u0026#233;', 'e').replace('\u0026#237;', 'i')
    
    # Pattern with scorers in parentheses
    pattern1 = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d(]+?)\s+(\d+)\s*\([^)]*\)\s*,\s*([^\d(]+?)\s+(\d+)(?:\s|$)'
    
    # Pattern without scorers
    pattern2 = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d,]+?)\s+(\d+)\s*,\s*([^\d(]+?)\s+(\d+)(?:\s|$)'
    
    for pattern in [pattern1, pattern2]:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            try:
                date = match.group(1)
                home_team = clean_team_name(match.group(3))
                home_score = match.group(4)
                away_team = clean_team_name(match.group(5))
                away_score = match.group(6)
                
                if not home_score or not away_score:
                    continue
                
                # Check if Independiente Avellaneda is playing
                home_is_ind = is_independiente_avellaneda(home_team)
                away_is_ind = is_independiente_avellaneda(away_team)
                
                if home_is_ind or away_is_ind:
                    try:
                        h_score = int(home_score)
                        a_score = int(away_score)
                        
                        # Determine result from Independiente's perspective
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
                        
                        # Standardize team names
                        if home_is_ind:
                            home_team = "Independiente"
                        if away_is_ind:
                            away_team = "Independiente"
                        
                        matches.append({
                            'date': date,
                            'competition': default_competition,
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

def scrape_post(url, default_competition):
    soup = fetch_page(url)
    if not soup:
        return []
    
    text = soup.get_text()
    matches = extract_matches_from_text(text, default_competition)
    return matches

def main():
    all_matches = []
    
    for year, urls in URLS.items():
        print(f"\n{'='*60}")
        print(f"Year {year}")
        print('='*60)
        
        year_matches = []
        for url, competition in urls:
            print(f"Scraping: {competition}")
            matches = scrape_post(url, competition)
            if matches:
                print(f"  Found {len(matches)} matches")
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
    output_file = 'independiente_matches_2011_2019.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        writer.writeheader()
        writer.writerows(unique_matches)
    
    print(f"\n{'='*60}")
    print(f"Total unique matches: {len(unique_matches)}")
    print(f"Data saved to {output_file}")
    
    # Print summary by year
    print("\n=== Summary by Year ===")
    year_counts = {}
    for match in unique_matches:
        year = match['date'].split('/')[-1]
        year_counts[year] = year_counts.get(year, 0) + 1
    
    for year in sorted(year_counts.keys()):
        print(f"  {year}: {year_counts[year]} matches")

if __name__ == "__main__":
    main()
