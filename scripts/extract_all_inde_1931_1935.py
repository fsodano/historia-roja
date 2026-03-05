#!/usr/bin/env python3
"""
Extract ALL Club Atlético Independiente matches from the blog content for years 1931-1935.
Parses match lines in format: "DD/MM/YYYY en Location: Team1 X, Team2 Y"
"""

import re
import csv
from pathlib import Path

# Match pattern to capture date, location, team1, score1, team2, score2
MATCH_PATTERN = re.compile(
    r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^,]+?)\s+(\d+)\s*,\s*([^,]+?)\s+(\d+)'
)

def extract_all_matches(text):
    """Extract all matches from text."""
    matches = []
    lines = text.split('\n')
    
    for line in lines:
        # Find all match patterns in the line
        for match in MATCH_PATTERN.finditer(line):
            date_str, location, team1, score1, team2, score2 = match.groups()
            
            # Clean up team names
            team1 = team1.strip()
            team2 = team2.strip()
            
            # Check if Independiente is in either team
            if "Independiente" not in team1 and "Independiente" not in team2:
                continue
            
            # Extract year
            year = date_str.split('/')[-1]
            if year not in ['1931', '1932', '1933', '1934', '1935']:
                continue
            
            home_team = team1
            away_team = team2
            home_score = int(score1)
            away_score = int(score2)
            
            # Determine result from Independiente's perspective
            independiente_home = "Independiente" in team1
            if independiente_home:
                if home_score > away_score:
                    result = "WIN"
                elif home_score < away_score:
                    result = "LOSS"
                else:
                    result = "DRAW"
            else:
                if away_score > home_score:
                    result = "WIN"
                elif away_score < home_score:
                    result = "LOSS"
                else:
                    result = "DRAW"
            
            # Determine competition based on context
            competition = "Primera División"
            if 'copa de honor' in line.lower() or 'beccar varela' in line.lower():
                competition = "Copa de Honor"
            elif 'copa competencia' in line.lower():
                competition = "Copa Competencia"
            elif 'copa ibarguren' in line.lower():
                competition = "Copa Ibarguren"
            
            matches.append({
                'date': date_str,
                'competition': competition,
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score,
                'result': result
            })
    
    return matches

def main():
    # Read the content file directly
    content_file = Path("/Users/fsodano/.local/share/opencode/tool-output/tool_cbacf6f970011Ipu9eU7CEpWB9")
    
    if not content_file.exists():
        print(f"Content file not found: {content_file}")
        return
    
    with open(content_file, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Extract all matches
    all_matches = extract_all_matches(text)
    
    print(f"Found {len(all_matches)} total matches")
    
    # Group by year
    matches_by_year = {}
    for match in all_matches:
        year = match['date'].split('/')[-1]
        if year not in matches_by_year:
            matches_by_year[year] = []
        matches_by_year[year].append(match)
    
    # Sort matches within each year by date
    for year in matches_by_year:
        matches_by_year[year].sort(key=lambda x: x['date'])
    
    # Create output directory
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    # Write CSV for each year
    for year in ['1931', '1932', '1933', '1934', '1935']:
        if year in matches_by_year:
            matches = matches_by_year[year]
            output_file = output_dir / f"{year}.csv"
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
                writer.writeheader()
                writer.writerows(matches)
            print(f"Created {output_file} with {len(matches)} matches")
        else:
            # Create empty file with header
            output_file = output_dir / f"{year}.csv"
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
                writer.writeheader()
            print(f"Created {output_file} with 0 matches (no data found)")
    
    print(f"\nTotal Independiente matches found: {len(all_matches)}")
    for year in ['1931', '1932', '1933', '1934', '1935']:
        count = len(matches_by_year.get(year, []))
        print(f"  {year}: {count} matches")

if __name__ == "__main__":
    main()
