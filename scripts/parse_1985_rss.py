#!/usr/bin/env python3
"""
Parse 1985 Atom feed and extract Independiente (Avellaneda) matches
"""

import xml.etree.ElementTree as ET
import html
import re
import csv

def extract_independiente_matches(xml_file, output_csv):
    """Extract Club Atlético Independiente matches from RSS feed"""
    
    with open(xml_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    root = ET.fromstring(xml_content)
    
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'blogger': 'http://schemas.google.com/blogger/2008',
    }
    
    matches = []
    
    for entry in root.findall('atom:entry', ns):
        title_elem = entry.find('atom:title', ns)
        content_elem = entry.find('atom:content', ns)
        
        if content_elem is not None and content_elem.text:
            content = html.unescape(content_elem.text)
            title = html.unescape(title_elem.text) if title_elem is not None else ''
            
            # Skip if not about Independiente (Avellaneda)
            # Look for matches with pattern: DD/MM/YYYY en Location: Team1 X, Team2 Y
            match_pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s+([^,]+?)\s+(\d+)\s*,\s*([^,]+?)\s+(\d+)'
            
            for match in re.finditer(match_pattern, content):
                date_str = match.group(1)
                location = match.group(2).strip()
                team1 = match.group(3).strip()
                score1 = int(match.group(4))
                team2 = match.group(5).strip()
                score2 = int(match.group(6))
                
                # Check if it's Club Atlético Independiente (Avellaneda) - the famous club
                team1_lower = team1.lower()
                team2_lower = team2.lower()
                
                is_independiente = False
                
                # Must be exactly "Independiente" or contain "(Avellaneda)"
                # Exclude regional clubs like "Independiente de La Rioja", "Independiente de Río Gallegos", etc.
                if team1_lower == 'independiente' or 'independiente (avellaneda)' in team1_lower:
                    is_independiente = True
                    ind_is_home = True
                elif team2_lower == 'independiente' or 'independiente (avellaneda)' in team2_lower:
                    is_independiente = True
                    ind_is_home = False
                
                if is_independiente:
                    if ind_is_home:
                        home_team = team1
                        away_team = team2
                        home_score = score1
                        away_score = score2
                        ind_score = score1
                        opp_score = score2
                    else:
                        home_team = team1
                        away_team = team2
                        home_score = score1
                        away_score = score2
                        ind_score = score2
                        opp_score = score1
                    
                    if ind_score > opp_score:
                        result = 'WIN'
                    elif ind_score < opp_score:
                        result = 'LOSS'
                    else:
                        result = 'DRAW'
                    
                    # Extract competition
                    competition = 'Primera División'
                    title_lower = title.lower()
                    if 'campeonato nacional' in title_lower:
                        competition = 'Campeonato Nacional'
                    elif 'copa' in title_lower:
                        if 'copa de honor' in title_lower:
                            competition = 'Copa de Honor'
                        elif 'copa competencia' in title_lower:
                            competition = 'Copa Competencia'
                        elif 'copa libertadores' in title_lower:
                            competition = 'Copa Libertadores'
                        else:
                            copa_match = re.search(r'Copa\s+([\w\s]+)', title, re.IGNORECASE)
                            if copa_match:
                                competition = f"Copa {copa_match.group(1).strip()}"
                    
                    matches.append({
                        'date': date_str,
                        'competition': competition,
                        'home_team': home_team,
                        'away_team': away_team,
                        'home_score': home_score,
                        'away_score': away_score,
                        'result': result
                    })
    
    # Remove duplicates (same match might appear in multiple entries)
    seen = set()
    unique_matches = []
    for m in matches:
        key = (m['date'], m['home_team'], m['away_team'], m['home_score'], m['away_score'])
        if key not in seen:
            seen.add(key)
            unique_matches.append(m)
    
    # Sort by date
    unique_matches.sort(key=lambda x: x['date'])
    
    # Save to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        writer.writeheader()
        writer.writerows(unique_matches)
    
    print(f"Extracted {len(unique_matches)} matches to {output_csv}")
    
    # Show matches
    if unique_matches:
        print("\nIndependiente (Avellaneda) matches in 1985:")
        for i, m in enumerate(unique_matches, 1):
            print(f"{i}. {m['date']} | {m['competition']} | {m['home_team']} {m['home_score']}-{m['away_score']} {m['away_team']} | {m['result']}")
    
    return unique_matches

if __name__ == "__main__":
    xml_file = '/Users/fsodano/.local/share/opencode/tool-output/tool_cbc0d63d7001Cc9q5An9zEIUyQ'
    output_csv = 'data/1985-rss.csv'
    extract_independiente_matches(xml_file, output_csv)
