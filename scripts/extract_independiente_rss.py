#!/usr/bin/env python3
"""
Extract Club Atlético Independiente matches from RSS feed for a given year
Usage: python extract_independiente_rss.py <year>
"""

import sys
import requests
import xml.etree.ElementTree as ET
import html
import re
import csv

def fetch_and_parse_year(year):
    """Fetch RSS feed and extract Independiente matches for a given year"""
    
    url = f"https://josecarluccio.blogspot.com/feeds/posts/default/-/{year}?max-results=200"
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        xml_content = response.text
    except Exception as e:
        print(f"Error fetching {year}: {e}")
        return []
    
    root = ET.fromstring(xml_content)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    matches = []
    
    for entry in root.findall('atom:entry', ns):
        title_elem = entry.find('atom:title', ns)
        content_elem = entry.find('atom:content', ns)
        
        if content_elem is not None and content_elem.text:
            content = html.unescape(content_elem.text)
            title = html.unescape(title_elem.text) if title_elem is not None else ''
            
            # Pattern: DD/MM/YYYY en Location: Team X, Team Y Y
            match_pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s+([^,(]+?)\s+(\d+)\s*(?:\([^)]*\))?\s*,\s*([^,(]+?)\s+(\d+)'
            
            for match in re.finditer(match_pattern, content):
                date_str = match.group(1)
                team1 = match.group(3).strip()
                score1 = int(match.group(4))
                team2 = match.group(5).strip()
                score2 = int(match.group(6))
                
                team1_lower = team1.lower()
                team2_lower = team2.lower()
                
                # Check for Club Atlético Independiente (Avellaneda) only
                is_independiente = False
                if team1_lower == 'independiente' or 'independiente (avellaneda)' in team1_lower:
                    is_independiente = True
                    ind_is_home = True
                elif team2_lower == 'independiente' or 'independiente (avellaneda)' in team2_lower:
                    is_independiente = True
                    ind_is_home = False
                
                if is_independiente:
                    home_team = team1
                    away_team = team2
                    home_score = score1
                    away_score = score2
                    
                    ind_score = home_score if ind_is_home else away_score
                    opp_score = away_score if ind_is_home else home_score
                    
                    if ind_score > opp_score:
                        result = 'WIN'
                    elif ind_score < opp_score:
                        result = 'LOSS'
                    else:
                        result = 'DRAW'
                    
                    # Determine competition
                    competition = 'Primera División'
                    title_lower = title.lower()
                    if 'campeonato nacional' in title_lower:
                        competition = 'Campeonato Nacional'
                    elif 'copa de honor' in title_lower:
                        competition = 'Copa de Honor'
                    elif 'copa competencia' in title_lower:
                        competition = 'Copa Competencia'
                    elif 'copa libertadores' in title_lower:
                        competition = 'Copa Libertadores'
                    elif 'copa' in title_lower:
                        competition = 'Copa'
                    elif 'metropolitano' in title_lower:
                        competition = 'Campeonato Metropolitano'
                    
                    matches.append({
                        'date': date_str,
                        'competition': competition,
                        'home_team': home_team,
                        'away_team': away_team,
                        'home_score': home_score,
                        'away_score': away_score,
                        'result': result
                    })
    
    # Remove duplicates and sort
    seen = set()
    unique_matches = []
    for m in matches:
        key = (m['date'], m['home_team'], m['away_team'])
        if key not in seen:
            seen.add(key)
            unique_matches.append(m)
    
    unique_matches.sort(key=lambda x: x['date'])
    return unique_matches

def save_to_csv(matches, year):
    """Save matches to CSV"""
    if not matches:
        print(f"No matches found for {year}")
        return
    
    filename = f"data/{year}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        writer.writeheader()
        writer.writerows(matches)
    
    print(f"Saved {len(matches)} matches to {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_independiente_rss.py <year>")
        sys.exit(1)
    
    year = sys.argv[1]
    print(f"Fetching matches for {year}...")
    matches = fetch_and_parse_year(year)
    save_to_csv(matches, year)
    print(f"Done! Found {len(matches)} matches.")
