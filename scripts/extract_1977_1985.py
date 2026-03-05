#!/usr/bin/env python3
"""
Extract Club Atlético Independiente matches from josecarluccio.blogspot.com for years 1977-1985.
"""

import re
import csv
from datetime import datetime

# Match data extracted from blog - format: date, competition, match_line
matches_data = {
    1978: [
        # Campeonato Nacional 1978 - Zona C
        ("05/11/1978", "Campeonato Nacional", "05/11/1978 en General Roca: Deportivo Roca de Río Negro 0, Independiente 2"),
        ("08/11/1978", "Campeonato Nacional", "08/11/1978 en Avellaneda: Independiente 2, Vélez Sarsfield 2"),
        ("12/11/1978", "Campeonato Nacional", "12/11/1978 en Paternal: Argentinos Juniors 0, Independiente 1"),
        ("15/11/1978", "Campeonato Nacional", "15/11/1978 en Avellaneda: Independiente 1, Rosario Central 0"),
        ("19/11/1978", "Campeonato Nacional", "19/11/1978 en La Plata: Gimnasia y Esgrima La Plata 2, Independiente 1"),
        ("22/11/1978", "Campeonato Nacional", "22/11/1978 en Avellaneda: Independiente 3, Racing de Córdoba 1"),
        ("26/11/1978", "Campeonato Nacional", "26/11/1978 en Palpalá: Altos Hornos Zapla de Jujuy 1, Independiente 4"),
        ("29/11/1978", "Campeonato Nacional", "29/11/1978 en Avellaneda: Independiente 4, Deportivo Roca de Río Negro 1"),
        ("03/12/1978", "Campeonato Nacional", "03/12/1978 en Liniers: Vélez Sarsfield 2, Independiente 1"),
        ("06/12/1978", "Campeonato Nacional", "06/12/1978 en Avellaneda: Independiente 4, Argentinos Juniors 2"),
        ("09/12/1978", "Campeonato Nacional", "09/12/1978 en Rosario: Rosario Central 2, Independiente 2"),
        ("13/12/1978", "Campeonato Nacional", "13/12/1978 en Avellaneda: Independiente 3, Gimnasia y Esgrima La Plata 1"),
        ("17/12/1978", "Campeonato Nacional", "17/12/1978 en Córdoba: Racing de Córdoba 1, Independiente 1"),
        ("20/12/1978", "Campeonato Nacional", "20/12/1978 en Avellaneda: Independiente 2, Altos Hornos Zapla de Jujuy 1"),
    ],
    1979: [
        # Campeonato Metropolitano 1979 - Zona B
        ("05/03/1979", "Campeonato Metropolitano", "05/03/1979 en Avellaneda: Independiente 1, Ferro Carril Oeste 3"),
        ("11/03/1979", "Campeonato Metropolitano", "11/03/1979 en Avellaneda: Independiente 1, All Boys 2"),
        ("17/03/1979", "Campeonato Metropolitano", "17/03/1979 en Villa Crespo: Atlanta 1, Independiente 2"),
        ("25/03/1979", "Campeonato Metropolitano", "25/03/1979 en Avellaneda: Independiente 1, Rosario Central 2"),
        ("01/04/1979", "Campeonato Metropolitano", "01/04/1979 en Boedo: San Lorenzo 2, Independiente 2"),
        ("08/04/1979", "Campeonato Metropolitano", "08/04/1979 en Avellaneda: Independiente 1, Boca Juniors 0"),
        ("15/04/1979", "Campeonato Metropolitano", "15/04/1979 en San Martín: Chacarita Juniors 2, Independiente 1"),
        ("22/04/1979", "Campeonato Metropolitano", "22/04/1979 en Avellaneda: Independiente 5, Estudiantes de La Plata 3"),
        ("29/04/1979", "Campeonato Metropolitano", "29/04/1979 en Santa Fe: Colón 2, Independiente 3"),
        ("02/05/1979", "Campeonato Metropolitano", "02/05/1979 en Liniers: Ferro Carril Oeste 0, Independiente 4"),
        ("06/05/1979", "Campeonato Metropolitano", "06/05/1979 en Floresta: All Boys 0, Independiente 2"),
        ("13/05/1979", "Campeonato Metropolitano", "13/05/1979 en Avellaneda: Independiente 1, Atlanta 0"),
        ("10/06/1979", "Campeonato Metropolitano", "10/06/1979 en Rosario: Rosario Central 4, Independiente 2"),
        ("17/06/1979", "Campeonato Metropolitano", "17/06/1979 en Avellaneda: Independiente 3, San Lorenzo 2"),
        ("23/06/1979", "Campeonato Metropolitano", "23/06/1979 en La Boca: Boca Juniors 0, Independiente 0"),
        ("01/07/1979", "Campeonato Metropolitano", "01/07/1979 en Avellaneda: Independiente 2, Chacarita Juniors 1"),
        ("08/07/1979", "Campeonato Metropolitano", "08/07/1979 en La Plata: Estudiantes de La Plata 1, Independiente 3"),
        ("15/07/1979", "Campeonato Metropolitano", "15/07/1979 en Avellaneda: Independiente 2, Colón 0"),
    ],
}

def parse_match_line(date_str, competition, match_line):
    """Parse a match line and extract match details."""
    # Pattern: DD/MM/YYYY en Location: Team1 X, Team2 Y
    pattern = r'\d{2}/\d{2}/\d{4} en ([^:]+):\s*([^,]+),\s*([^\(]+)'
    match = re.search(pattern, match_line)
    
    if not match:
        return None
    
    location = match.group(1).strip()
    team1_part = match.group(2).strip()
    team2_part = match.group(3).strip()
    
    # Extract team names and scores
    # Team name might have "de" in it, so we need to be careful
    # Format: TeamName Score or TeamName Score (scorers...)
    
    def extract_team_and_score(part):
        # Remove goal scorer info in parentheses
        part = re.sub(r'\s*\([^)]*\)\s*$', '', part).strip()
        # Find the last number (score)
        score_match = re.search(r'(\d+)\s*$', part)
        if score_match:
            score = int(score_match.group(1))
            team = part[:score_match.start()].strip()
            return team, score
        return part, None
    
    team1, score1 = extract_team_and_score(team1_part)
    team2, score2 = extract_team_and_score(team2_part)
    
    if score1 is None or score2 is None:
        return None
    
    # Determine home/away based on "en" location
    # If location contains the first team's city, team1 is home
    # Otherwise, we need to infer
    
    # Check if Independiente is team1 or team2
    ind_is_team1 = 'independiente' in team1.lower()
    ind_is_team2 = 'independiente' in team2.lower()
    
    if ind_is_team1:
        home_team = team1
        away_team = team2
        home_score = score1
        away_score = score2
    elif ind_is_team2:
        home_team = team1
        away_team = team2
        home_score = score1
        away_score = score2
    else:
        return None  # Independiente not in this match
    
    # Determine result from Independiente's perspective
    if ind_is_team1:
        if score1 > score2:
            result = "WIN"
        elif score1 < score2:
            result = "LOSS"
        else:
            result = "DRAW"
    else:  # ind_is_team2
        if score2 > score1:
            result = "WIN"
        elif score2 < score1:
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

def write_csv(year, matches):
    """Write matches to CSV file."""
    filepath = f'/Users/fsodano/fibradev/historia-roja/data/{year}.csv'
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        
        for match in matches:
            writer.writerow([
                match['date'],
                match['competition'],
                match['home_team'],
                match['away_team'],
                match['home_score'],
                match['away_score'],
                match['result']
            ])
    
    return len(matches)

def main():
    summary = []
    
    for year in [1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985]:
        matches = []
        
        if year in matches_data:
            for date_str, competition, match_line in matches_data[year]:
                parsed = parse_match_line(date_str, competition, match_line)
                if parsed:
                    matches.append(parsed)
        
        # Sort matches by date
        matches.sort(key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y'))
        
        if matches:
            count = write_csv(year, matches)
            summary.append(f"  {year}: {count} matches")
        else:
            # Create empty CSV with headers
            write_csv(year, [])
            summary.append(f"  {year}: 0 matches")
    
    print("\nSummary of matches extracted:")
    print("\n".join(summary))
    print("\nAll CSV files created successfully!")

if __name__ == '__main__':
    main()
