#!/usr/bin/env python3
import re
import csv
from pathlib import Path

def clean_text(text):
    text = text.replace('&#8217;', "'")
    text = text.replace('&#8211;', '-')
    text = text.replace('&#8220;', '"')
    text = text.replace('&#8221;', '"')
    text = text.replace('&#8230;', '...')
    text = text.replace('&nbsp;', ' ')
    return text

def extract_matches(text):
    """Extract all matches from text using regex."""
    # Pattern: DD/MM/YYYY en Location: Team1 SCORE, Team2 SCORE
    # Score is a number that is NOT followed immediately by a letter (like "5ta")
    # After score we expect: space, (, comma, or end of match
    # Use word boundary with negative lookahead for letters
    pattern = r'(\d{1,2}/\d{1,2}/\d{4}) en ([^:]+):\s*([^(,\d]+?)\s+(\d{1,2})\b(?!\w)\s*(?:\([^)]*\))?\s*,\s*([^(,\d]+?)\s+(\d{1,2})\b(?!\w)'

    matches = []
    for match in re.finditer(pattern, text):
        date, location, team1, score1, team2, score2 = match.groups()
        matches.append({
            'date': date.strip(),
            'location': location.strip(),
            'team1': team1.strip(),
            'team2': team2.strip(),
            'score1': int(score1),
            'score2': int(score2),
            'full_match': match.group(0)
        })
    return matches

def extract_independiente_matches(text):
    """Extract all matches where Independiente played."""
    text = clean_text(text)

    comp_markers = [
        (r'Copa de Competencia Británica', 'Copa de Competencia Británica'),
        (r'Copa Adrián C\. Escobar', 'Copa Adrián C. Escobar'),
        (r'Copa de Honor', 'Copa de Honor'),
        (r'Copa Competencia', 'Copa Competencia'),
        (r'Copa Ibarguren', 'Copa Ibarguren'),
        (r'Copa General Pedro Pablo Ramírez', 'Copa General Pedro Pablo Ramírez'),
        (r'Campeonato Rioplatense', 'Campeonato Rioplatense'),
    ]

    all_matches = extract_matches(text)
    independiente_matches = []

    for match in all_matches:
        if 'Independiente' in match['team1'] or 'Independiente' in match['team2']:
            match_pos = text.find(match['full_match'])
            section_start = max(0, match_pos - 2000)
            section = text[section_start:match_pos]

            competition = "Primera División"
            for pattern, comp_name in comp_markers:
                if re.search(pattern, section):
                    competition = comp_name
                    break

            home_team = match['team1']
            away_team = match['team2']
            home_score = match['score1']
            away_score = match['score2']

            if 'Independiente' in match['team1']:
                result = 'WIN' if home_score > away_score else ('LOSS' if home_score < away_score else 'DRAW')
            else:
                result = 'WIN' if away_score > home_score else ('LOSS' if away_score < home_score else 'DRAW')

            independiente_matches.append({
                'date': match['date'],
                'competition': competition,
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score,
                'result': result
            })

    return independiente_matches

def process_year(year, input_file, output_file):
    print(f"Processing {year}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    matches = extract_independiente_matches(content)
    print(f"  Found {len(matches)} Independiente matches")

    if matches:
        print(f"  Sample: {matches[0]}")

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        writer.writeheader()
        writer.writerows(matches)

    return len(matches)

def main():
    years = ['1946', '1947', '1948', '1949', '1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960']
    input_dir = Path('/Users/fsodano/.local/share/opencode/tool-output')
    output_dir = Path('/Users/fsodano/fibradev/historia-roja/data')
    output_dir.mkdir(exist_ok=True)

    input_files = sorted(input_dir.glob('tool_*'))
    print(f"Found {len(input_files)} input files")

    total_matches = 0
    year_file_map = {}

    for year in years:
        for input_file in input_files:
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if f'historiayfutbol: {year}' in content[:500]:
                        year_file_map[year] = input_file
                        break
            except:
                continue

    for year in years:
        if year in year_file_map:
            count = process_year(year, year_file_map[year], output_dir / f'{year}.csv')
            total_matches += count
        else:
            print(f"  Warning: No data found for {year}")

    print(f"\nTotal matches extracted: {total_matches}")

if __name__ == '__main__':
    main()
