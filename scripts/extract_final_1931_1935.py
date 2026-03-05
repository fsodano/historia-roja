#!/usr/bin/env python3
import re
import csv
from pathlib import Path

MATCH_PATTERN = re.compile(
    r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^,]+?)\s+(\d+)\s*,\s*([^,]+?)\s+(\d+)'
)

def extract_all_matches(text, default_competition="Primera División"):
    matches = []
    lines = text.split('\n')
    current_competition = default_competition
    
    for line in lines:
        if 'Copa de Honor' in line or 'Beccar Varela' in line:
            current_competition = 'Copa de Honor'
        elif 'Copa Competencia' in line:
            current_competition = 'Copa Competencia'
        elif 'Copa Ibarguren' in line:
            current_competition = 'Copa Ibarguren'
        elif 'Primera División' in line or '1ra. División' in line:
            current_competition = 'Primera División'
        
        for match in MATCH_PATTERN.finditer(line):
            date_str, location, team1, score1, team2, score2 = match.groups()
            team1 = team1.strip()
            team2 = team2.strip()
            
            if "Independiente" not in team1 and "Independiente" not in team2:
                continue
            
            year = date_str.split('/')[-1]
            if year not in ['1931', '1932', '1933', '1934', '1935']:
                continue
            
            home_team = team1
            away_team = team2
            home_score = int(score1)
            away_score = int(score2)
            
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
            
            competition = current_competition
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
    tool_output_dir = Path("/Users/fsodano/.local/share/opencode/tool-output")
    all_matches = []
    
    files = sorted(tool_output_dir.glob("tool_cbac*"), key=lambda p: p.stat().st_mtime, reverse=True)[:100]
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            matches = extract_all_matches(text)
            if matches:
                all_matches.extend(matches)
        except Exception:
            pass
    
    seen = set()
    unique_matches = []
    for match in all_matches:
        key = (match['date'], match['home_team'], match['away_team'], match['home_score'], match['away_score'])
        if key not in seen:
            seen.add(key)
            unique_matches.append(match)
    
    all_matches = unique_matches
    all_matches.sort(key=lambda x: x['date'])
    
    matches_by_year = {}
    for match in all_matches:
        year = match['date'].split('/')[-1]
        if year not in matches_by_year:
            matches_by_year[year] = []
        matches_by_year[year].append(match)
    
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    for year in ['1931', '1932', '1933', '1934', '1935']:
        output_file = output_dir / f"{year}.csv"
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
            writer.writeheader()
            if year in matches_by_year:
                writer.writerows(matches_by_year[year])
                print(f"Created {output_file} with {len(matches_by_year[year])} matches")
            else:
                print(f"Created {output_file} with 0 matches")
    
    print(f"\nTotal Independiente matches found: {len(all_matches)}")
    for year in ['1931', '1932', '1933', '1934', '1935']:
        count = len(matches_by_year.get(year, []))
        print(f"  {year}: {count} matches")

if __name__ == "__main__":
    main()
