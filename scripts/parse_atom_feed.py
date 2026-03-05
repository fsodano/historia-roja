#!/usr/bin/env python3
"""
Parse Atom feed from josecarluccio.blogspot.com and extract Independiente matches
"""

import xml.etree.ElementTree as ET
import html
import re
import csv
from datetime import datetime

def parse_atom_feed(xml_content):
    """Parse Atom feed and extract match data"""
    
    # Parse XML
    root = ET.fromstring(xml_content)
    
    # Define namespaces
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'blogger': 'http://schemas.google.com/blogger/2008',
        'media': 'http://search.yahoo.com/mrss/'
    }
    
    matches = []
    
    # Find all entry elements
    for entry in root.findall('atom:entry', ns):
        # Get title and content
        title = entry.find('atom:title', ns)
        content = entry.find('atom:content', ns)
        
        if content is not None and content.text:
            # Decode HTML entities
            decoded_content = html.unescape(content.text)
            
            # Look for matches in the content
            # Pattern: "DD/MM/YYYY en Location: Team1 X, Team2 Y"
            match_pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s+([^,]+)\s+(\d+)\s*,\s*([^,]+)\s+(\d+)'
            
            for match in re.finditer(match_pattern, decoded_content):
                date_str = match.group(1)
                location = match.group(2).strip()
                team1 = match.group(3).strip()
                score1 = int(match.group(4))
                team2 = match.group(5).strip()
                score2 = int(match.group(6))
                
                # Check if Independiente is playing
                if 'independiente' in team1.lower() or 'independiente' in team2.lower():
                    match_data = extract_match_data(date_str, location, team1, score1, team2, score2, title.text if title is not None else '')
                    if match_data:
                        matches.append(match_data)
    
    return matches

def extract_match_data(date_str, location, team1, score1, team2, score2, title):
    """Extract match data with home/away determination"""
    
    # Determine if Independiente is home or away
    if 'independiente' in team1.lower():
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
    
    # Determine result
    if ind_score > opp_score:
        result = 'WIN'
    elif ind_score < opp_score:
        result = 'LOSS'
    else:
        result = 'DRAW'
    
    # Extract competition from title
    competition = 'Primera División'
    if 'copa' in title.lower():
        if 'copa de honor' in title.lower():
            competition = 'Copa de Honor'
        elif 'copa competencia' in title.lower():
            competition = 'Copa Competencia'
        elif 'copa libertadores' in title.lower():
            competition = 'Copa Libertadores'
        else:
            # Extract Copa name
            copa_match = re.search(r'Copa\s+([\w\s]+)', title, re.IGNORECASE)
            if copa_match:
                competition = f"Copa {copa_match.group(1).strip()}"
    elif 'campeonato' in title.lower():
        if 'nacional' in title.lower():
            competition = 'Campeonato Nacional'
        elif 'metropolitano' in title.lower():
            competition = 'Campeonato Metropolitano'
    
    return {
        'date': date_str,
        'competition': competition,
        'home_team': home_team,
        'away_team': away_team,
        'home_score': home_score,
        'away_score': away_score,
        'result': result
    }

def save_matches_to_csv(matches, filename):
    """Save matches to CSV file"""
    if not matches:
        print(f"No matches found")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        writer.writeheader()
        writer.writerows(matches)
    
    print(f"Saved {len(matches)} matches to {filename}")

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python parse_atom_feed.py <input.xml> <output.csv>")
        sys.exit(1)
    
    # Read XML file
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    # Parse and extract matches
    matches = parse_atom_feed(xml_content)
    
    # Save to CSV
    save_matches_to_csv(matches, sys.argv[2])
