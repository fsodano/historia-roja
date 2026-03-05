#!/usr/bin/env python3
"""
Extract Club Atlético Independiente matches from the blog content for years 1931-1935.
Parses match lines in format: "DD/MM/YYYY en Location: Team1 X, Team2 Y"
"""

import re
import csv
import os
from pathlib import Path

# Match pattern to capture date, location, team1, score1, team2, score2
# Format: "DD/MM/YYYY en Location: Team1 X, Team2 Y"
MATCH_PATTERN = re.compile(
    r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^,]+?)\s+(\d+)\s*,\s*([^,]+?)\s+(\d+)'
)

def determine_competition(line_context):
    """Determine competition based on context."""
    line_lower = line_context.lower()
    
    if 'copa de honor' in line_lower or 'beccar varela' in line_lower:
        return 'Copa de Honor'
    elif 'copa competencia' in line_lower:
        return 'Copa Competencia'
    elif 'copa ibarguren' in line_lower:
        return 'Copa Ibarguren'
    elif 'primera division' in line_lower or '1ra. division' in line_lower:
        return 'Primera División'
    elif 'liga argentina' in line_lower:
        return 'Primera División'
    
    return 'Primera División'  # Default

def parse_match_line(line, competition="Primera División"):
    """Parse a match line and return match data if it contains Independiente."""
    match = MATCH_PATTERN.search(line)
    if not match:
        return None
    
    date_str, location, team1, score1, team2, score2 = match.groups()
    
    # Clean up team names
    team1 = team1.strip()
    team2 = team2.strip()
    
    # Check if Independiente is in either team
    if "Independiente" not in team1 and "Independiente" not in team2:
        return None
    
    # The team listed FIRST is the home team
    home_team = team1
    away_team = team2
    home_score = int(score1)
    away_score = int(score2)
    
    # Determine if Independiente is home or away
    independiente_home = "Independiente" in team1
    
    # Determine result from Independiente's perspective
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
    
    return {
        'date': date_str,
        'competition': competition,
        'home_team': home_team,
        'away_team': away_team,
        'home_score': home_score,
        'away_score': away_score,
        'result': result
    }

def extract_matches_from_text(text, default_competition="Primera División"):
    """Extract all Independiente matches from text."""
    matches = []
    lines = text.split('\n')
    
    current_competition = default_competition
    
    for line in lines:
        # Check for competition markers
        if 'Copa de Honor' in line or 'Beccar Varela' in line:
            current_competition = 'Copa de Honor'
        elif 'Copa Competencia' in line:
            current_competition = 'Copa Competencia'
        elif 'Copa Ibarguren' in line:
            current_competition = 'Copa Ibarguren'
        elif 'Primera División' in line or '1ra. División' in line:
            current_competition = 'Primera División'
        
        match = parse_match_line(line, current_competition)
        if match:
            matches.append(match)
    
    return matches

def extract_matches_from_file(filepath):
    """Extract matches from a file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    return extract_matches_from_text(text)

def main():
    # Directory containing the blog content files
    tool_output_dir = Path("/Users/fsodano/.local/share/opencode/tool-output")
    
    # Extract matches from all relevant files
    all_matches = []
    
    # Get all files from the tool output directory (recent ones)
    files = sorted(tool_output_dir.glob("tool_cbac*"), key=lambda p: p.stat().st_mtime, reverse=True)
    files = files[:50]  # Process most recent 50 files
    
    print(f"Processing {len(files)} files...")
    
    for filepath in files:
        try:
            matches = extract_matches_from_file(filepath)
            if matches:
                all_matches.extend(matches)
                print(f"Found {len(matches)} matches in {filepath.name}")
        except Exception as e:
            pass  # Silently skip problematic files
    
    # Remove duplicates based on date and opponent
    seen = set()
    unique_matches = []
    for match in all_matches:
        key = (match['date'], match['home_team'], match['away_team'], match['home_score'], match['away_score'])
        if key not in seen:
            seen.add(key)
            unique_matches.append(match)
    
    all_matches = unique_matches
    
    # Sort by date
    all_matches.sort(key=lambda x: x['date'])
    
    # Group by year
    matches_by_year = {}
    for match in all_matches:
        year = match['date'].split('/')[-1]
        if year not in matches_by_year:
            matches_by_year[year] = []
        matches_by_year[year].append(match)
    
    # Create output directory
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    # Write CSV for each year
    years_created = []
    for year in ['1931', '1932', '1933', '1934', '1935']:
        if year in matches_by_year:
            matches = matches_by_year[year]
            output_file = output_dir / f"{year}.csv"
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
                writer.writeheader()
                writer.writerows(matches)
            years_created.append((year, len(matches)))
            print(f"Created {output_file} with {len(matches)} matches")
        else:
            print(f"No matches found for year {year}")
    
    print(f"\nTotal matches found: {len(all_matches)}")
    for year, count in years_created:
        print(f"  {year}: {count} matches")

if __name__ == "__main__":
    main()
