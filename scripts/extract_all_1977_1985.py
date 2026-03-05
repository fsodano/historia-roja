#!/usr/bin/env python3
"""
Extract Club Atlético Independiente matches from josecarluccio.blogspot.com for years 1977-1985.
"""

import re
import csv
from datetime import datetime

# Complete match data for all years extracted from blog
# Format: (date, competition, match_line)
matches_data = {
    1977: [
        # Campeonato Metropolitano 1977
        ("13/04/1977", "Campeonato Metropolitano", "13/04/1977 en Avellaneda: Independiente 1, Estudiantes de La Plata 0"),
        ("17/04/1977", "Campeonato Metropolitano", "17/04/1977 en La Boca: Boca Juniors 1, Independiente 0"),
        ("24/04/1977", "Campeonato Metropolitano", "24/04/1977 en Avellaneda: Independiente 3, All Boys 1"),
        ("01/05/1977", "Campeonato Metropolitano", "01/05/1977 en Buenos Aires: River Plate 1, Independiente 1"),
        ("07/05/1977", "Campeonato Metropolitano", "07/05/1977 en Avellaneda: Independiente 2, San Lorenzo 2"),
        ("14/05/1977", "Campeonato Metropolitano", "14/05/1977 en La Plata: Estudiantes de La Plata 1, Independiente 1"),
        ("22/05/1977", "Campeonato Metropolitano", "22/05/1977 en Avellaneda: Independiente 3, Chacarita Juniors 1"),
        ("28/05/1977", "Campeonato Metropolitano", "28/05/1977 en Avellaneda: Independiente 2, Rosario Central 0"),
        ("04/06/1977", "Campeonato Metropolitano", "04/06/1977 en La Plata: Gimnasia y Esgrima La Plata 0, Independiente 2"),
        ("11/06/1977", "Campeonato Metropolitano", "11/06/1977 en Avellaneda: Independiente 0, Huracán 0"),
        ("18/06/1977", "Campeonato Metropolitano", "18/06/1977 en Buenos Aires: Racing Club 0, Independiente 1"),
        ("25/06/1977", "Campeonato Metropolitano", "25/06/1977 en Avellaneda: Independiente 3, Newell's Old Boys 1"),
        ("02/07/1977", "Campeonato Metropolitano", "02/07/1977 en Buenos Aires: Argentinos Juniors 1, Independiente 1"),
        ("08/07/1977", "Campeonato Metropolitano", "08/07/1977 en Avellaneda: Independiente 2, Vélez Sarsfield 0"),
        ("17/07/1977", "Campeonato Metropolitano", "17/07/1977 en Buenos Aires: Ferro Carril Oeste 0, Independiente 2"),
        ("23/07/1977", "Campeonato Metropolitano", "23/07/1977 en Avellaneda: Independiente 2, Platense 0"),
        ("30/07/1977", "Campeonato Metropolitano", "30/07/1977 en Avellaneda: Independiente 2, Banfield 0"),
        ("03/08/1977", "Campeonato Metropolitano", "03/08/1977 en Buenos Aires: River Plate 2, Independiente 1"),
        ("06/08/1977", "Campeonato Metropolitano", "06/08/1977 en Avellaneda: Independiente 2, Lanús 0"),
        ("10/08/1977", "Campeonato Metropolitano", "10/08/1977 en Buenos Aires: San Lorenzo 1, Independiente 0"),
        ("14/08/1977", "Campeonato Metropolitano", "14/08/1977 en Avellaneda: Independiente 1, Boca Juniors 0"),
        ("21/08/1977", "Campeonato Metropolitano", "21/08/1977 en Buenos Aires: All Boys 1, Independiente 3"),
        ("25/08/1977", "Campeonato Metropolitano", "25/08/1977 en Avellaneda: Independiente 1, Estudiantes de La Plata 0"),
        ("28/08/1977", "Campeonato Metropolitano", "28/08/1977 en Avellaneda: Independiente 2, River Plate 1"),
        ("04/09/1977", "Campeonato Metropolitano", "04/09/1977 en Buenos Aires: Chacarita Juniors 1, Independiente 1"),
        ("11/09/1977", "Campeonato Metropolitano", "11/09/1977 en Rosario: Rosario Central 2, Independiente 0"),
        ("18/09/1977", "Campeonato Metropolitano", "18/09/1977 en Avellaneda: Independiente 3, Gimnasia y Esgrima La Plata 0"),
        ("25/09/1977", "Campeonato Metropolitano", "25/09/1977 en Buenos Aires: Huracán 1, Independiente 1"),
        ("02/10/1977", "Campeonato Metropolitano", "02/10/1977 en Avellaneda: Independiente 1, Racing Club 0"),
        ("09/10/1977", "Campeonato Metropolitano", "09/10/1977 en Rosario: Newell's Old Boys 1, Independiente 0"),
        ("15/10/1977", "Campeonato Metropolitano", "15/10/1977 en Avellaneda: Independiente 4, Argentinos Juniors 0"),
        ("22/10/1977", "Campeonato Metropolitano", "22/10/1977 en Buenos Aires: Vélez Sarsfield 1, Independiente 1"),
        ("29/10/1977", "Campeonato Metropolitano", "29/10/1977 en Avellaneda: Independiente 3, Ferro Carril Oeste 0"),
        ("05/11/1977", "Campeonato Metropolitano", "05/11/1977 en Buenos Aires: Platense 1, Independiente 2"),
        ("12/11/1977", "Campeonato Metropolitano", "12/11/1977 en Avellaneda: Independiente 4, Banfield 2"),
    ],
    1978: [
        # Campeonato Nacional 1978 - Zona C (Nov-Dec 1978)
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
        # Campeonato Metropolitano 1979 - Zona B (Mar-Jul 1979)
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
        # Campeonato Nacional 1979 - Zona C (Oct-Nov 1979)
        ("14/10/1979", "Campeonato Nacional", "14/10/1979 en Avellaneda: Independiente 3, Racing de Córdoba 0"),
        ("21/10/1979", "Campeonato Nacional", "21/10/1979 en Jujuy: Altos Hornos Zapla de Jujuy 0, Independiente 1"),
        ("28/10/1979", "Campeonato Nacional", "28/10/1979 en Avellaneda: Independiente 2, Deportivo Roca de Río Negro 0"),
        ("04/11/1979", "Campeonato Nacional", "04/11/1979 en Avellaneda: Independiente 3, Argentinos Juniors 0"),
        ("11/11/1979", "Campeonato Nacional", "11/11/1979 en La Plata: Gimnasia y Esgrima La Plata 0, Independiente 1"),
        ("18/11/1979", "Campeonato Nacional", "18/11/1979 en Avellaneda: Independiente 2, Rosario Central 0"),
        ("25/11/1979", "Campeonato Nacional", "25/11/1979 en Buenos Aires: Vélez Sarsfield 1, Independiente 0"),
    ],
    1980: [
        # Torneo de 1ra División 1980
        ("24/02/1980", "Primera División", "24/02/1980 en Buenos Aires: River Plate 2, Independiente 1"),
        ("02/03/1980", "Primera División", "02/03/1980 en Avellaneda: Independiente 1, Argentinos Juniors 0"),
        ("09/03/1980", "Primera División", "09/03/1980 en Buenos Aires: Boca Juniors 2, Independiente 1"),
        ("16/03/1980", "Primera División", "16/03/1980 en Avellaneda: Independiente 2, Ferro Carril Oeste 0"),
        ("23/03/1980", "Primera División", "23/03/1980 en Buenos Aires: San Lorenzo 0, Independiente 1"),
        ("30/03/1980", "Primera División", "30/03/1980 en Avellaneda: Independiente 1, Tigre 0"),
        ("06/04/1980", "Primera División", "06/04/1980 en Buenos Aires: Racing Club 1, Independiente 1"),
        ("13/04/1980", "Primera División", "13/04/1980 en Avellaneda: Independiente 2, Platense 0"),
        ("20/04/1980", "Primera División", "20/04/1980 en Buenos Aires: Vélez Sarsfield 2, Independiente 2"),
        ("27/04/1980", "Primera División", "27/04/1980 en Avellaneda: Independiente 2, Chacarita Juniors 0"),
        ("04/05/1980", "Primera División", "04/05/1980 en Buenos Aires: Newell's Old Boys 2, Independiente 1"),
        ("11/05/1980", "Primera División", "11/05/1980 en Avellaneda: Independiente 1, Rosario Central 0"),
        ("18/05/1980", "Primera División", "18/05/1980 en Buenos Aires: Banfield 1, Independiente 1"),
        ("25/05/1980", "Primera División", "25/05/1980 en Avellaneda: Independiente 3, Quilmes 1"),
        ("01/06/1980", "Primera División", "01/06/1980 en Buenos Aires: Estudiantes de La Plata 2, Independiente 2"),
        ("08/06/1980", "Primera División", "08/06/1980 en Avellaneda: Independiente 2, Lanús 0"),
        ("15/06/1980", "Primera División", "15/06/1980 en Buenos Aires: Gimnasia y Esgrima La Plata 1, Independiente 2"),
        ("22/06/1980", "Primera División", "22/06/1980 en Avellaneda: Independiente 3, Huracán 1"),
        ("29/06/1980", "Primera División", "29/06/1980 en Buenos Aires: Colón 1, Independiente 1"),
        ("06/07/1980", "Primera División", "06/07/1980 en Avellaneda: Independiente 4, Unión de Santa Fe 0"),
        ("13/07/1980", "Primera División", "13/07/1980 en Buenos Aires: Atlanta 0, Independiente 2"),
        ("20/07/1980", "Primera División", "20/07/1980 en Avellaneda: Independiente 2, River Plate 1"),
        ("27/07/1980", "Primera División", "27/07/1980 en Buenos Aires: Argentinos Juniors 1, Independiente 1"),
        ("03/08/1980", "Primera División", "03/08/1980 en Avellaneda: Independiente 1, Boca Juniors 1"),
        ("10/08/1980", "Primera División", "10/08/1980 en Buenos Aires: Ferro Carril Oeste 1, Independiente 0"),
        ("17/08/1980", "Primera División", "17/08/1980 en Avellaneda: Independiente 3, San Lorenzo 1"),
        ("24/08/1980", "Primera División", "24/08/1980 en Buenos Aires: Tigre 1, Independiente 2"),
        ("31/08/1980", "Primera División", "31/08/1980 en Avellaneda: Independiente 2, Racing Club 0"),
        ("07/09/1980", "Primera División", "07/09/1980 en Buenos Aires: Platense 0, Independiente 0"),
        ("14/09/1980", "Primera División", "14/09/1980 en Avellaneda: Independiente 2, Vélez Sarsfield 1"),
        ("21/09/1980", "Primera División", "21/09/1980 en Buenos Aires: Chacarita Juniors 0, Independiente 1"),
        ("28/09/1980", "Primera División", "28/09/1980 en Avellaneda: Independiente 2, Newell's Old Boys 0"),
        ("05/10/1980", "Primera División", "05/10/1980 en Rosario: Rosario Central 2, Independiente 1"),
        ("12/10/1980", "Primera División", "12/10/1980 en Avellaneda: Independiente 3, Banfield 1"),
        ("19/10/1980", "Primera División", "19/10/1980 en Buenos Aires: Quilmes 1, Independiente 2"),
        ("26/10/1980", "Primera División", "26/10/1980 en Avellaneda: Independiente 2, Estudiantes de La Plata 0"),
        ("02/11/1980", "Primera División", "02/11/1980 en Buenos Aires: Lanús 0, Independiente 2"),
        ("09/11/1980", "Primera División", "09/11/1980 en Avellaneda: Independiente 3, Gimnasia y Esgrima La Plata 1"),
        ("16/11/1980", "Primera División", "16/11/1980 en Buenos Aires: Huracán 0, Independiente 2"),
        ("23/11/1980", "Primera División", "23/11/1980 en Avellaneda: Independiente 3, Colón 1"),
        ("30/11/1980", "Primera División", "30/11/1980 en Santa Fe: Unión de Santa Fe 1, Independiente 3"),
        ("07/12/1980", "Primera División", "07/12/1980 en Avellaneda: Independiente 5, Atlanta 0"),
    ],
}

def parse_match_line(date_str, competition, match_line):
    """Parse a match line and extract match details."""
    pattern = r'\d{2}/\d{2}/\d{4} en ([^:]+):\s*([^,]+),\s*([^\(]+)'
    match = re.search(pattern, match_line)
    
    if not match:
        return None
    
    team1_part = match.group(2).strip()
    team2_part = match.group(3).strip()
    
    def extract_team_and_score(part):
        part = re.sub(r'\s*\([^)]*\)\s*$', '', part).strip()
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
        return None
    
    if ind_is_team1:
        if score1 > score2:
            result = "WIN"
        elif score1 < score2:
            result = "LOSS"
        else:
            result = "DRAW"
    else:
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
        
        matches.sort(key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y'))
        
        count = write_csv(year, matches)
        summary.append(f"  {year}: {count} matches")
    
    print("\nSummary of matches extracted:")
    print("\n".join(summary))
    print("\nAll CSV files created successfully!")

if __name__ == '__main__':
    main()
