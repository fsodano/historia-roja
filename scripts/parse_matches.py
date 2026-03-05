import json
import re
from datetime import datetime

# Read the body text
with open('/Users/fsodano/fibradev/historia-roja/data/body_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Spanish month mapping
months_es = {
    'ene': '01', 'enero': '01',
    'feb': '02', 'febrero': '02',
    'mar': '03', 'marzo': '03',
    'abr': '04', 'abril': '04',
    'may': '05', 'mayo': '05',
    'jun': '06', 'junio': '06',
    'jul': '07', 'julio': '07',
    'ago': '08', 'agosto': '08',
    'sep': '09', 'sept': '09', 'septiembre': '09',
    'oct': '10', 'octubre': '10',
    'nov': '11', 'noviembre': '11',
    'dic': '12', 'diciembre': '12'
}

def parse_date(date_str):
    """Parse date like 'Dom., 23 de Oct.' to DD/MM/YYYY"""
    try:
        # Remove day name and clean up
        date_str = date_str.replace('Dom.,', '').replace('Lun.,', '').replace('Mar.,', '').replace('Mié.,', '').replace('Jue.,', '').replace('Vie.,', '').replace('Sáb.,', '').strip()
        date_str = date_str.replace('de', '').replace('.', '').strip()
        
        parts = date_str.split()
        if len(parts) >= 2:
            day = parts[0].zfill(2)
            month = parts[1].lower()
            month_num = months_es.get(month, '01')
            return f"{day}/{month_num}/2022"
    except:
        pass
    return date_str

def get_result(home_score, away_score, is_independiente_home):
    """Determine WIN/LOSS/DRAW from Independiente's perspective"""
    try:
        home = int(home_score)
        away = int(away_score)
        
        if home == away:
            return 'DRAW'
        
        if is_independiente_home:
            return 'WIN' if home > away else 'LOSS'
        else:
            return 'WIN' if away > home else 'LOSS'
    except:
        return 'DRAW'

# Find all match sections
matches = []

# Split by month headers
lines = text.split('\n')
current_date = None
current_competition = None

i = 0
while i < len(lines):
    line = lines[i].strip()
    
    # Check for date line (format: "Dom., 23 de Oct.")
    if re.match(r'^(Dom\.|Lun\.|Mar\.|Mié\.|Jue\.|Vie\.|Sáb\.)', line):
        current_date = line
        i += 1
        continue
    
    # Check for competition header
    if '2022' in line and ('FECHA' in line or 'PARTIDO' in line):
        i += 1
        continue
    
    # Look for score pattern (X - Y)
    if re.match(r'^\d+\s+-\s+\d+$', line):
        # Found a score line, extract the match
        # The pattern should be: team1, score line, team2
        # Go back to find teams
        if i >= 2:
            home_team = lines[i-1].strip()
            away_team = lines[i+1].strip() if i+1 < len(lines) else ''
            
            # Parse score
            score_parts = line.split('-')
            home_score = score_parts[0].strip()
            away_score = score_parts[1].strip()
            
            # Find competition (usually 2-3 lines after away team)
            competition = 'Liga Profesional de Fútbol'  # default
            for j in range(i+2, min(i+5, len(lines))):
                comp_line = lines[j].strip()
                if 'Finalizado' in comp_line or 'Final' in comp_line:
                    # Competition is on this line
                    if '\t' in comp_line:
                        comp_parts = comp_line.split('\t')
                        if len(comp_parts) > 1:
                            competition = comp_parts[-1].strip()
                    elif '  ' in comp_line:
                        comp_parts = comp_line.split('  ')
                        if len(comp_parts) > 1:
                            competition = comp_parts[-1].strip()
                    break
            
            # Determine if Independiente is home or away
            is_independiente_home = 'Independiente' in home_team
            
            match = {
                'date': parse_date(current_date) if current_date else '',
                'competition': competition,
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score,
                'result': get_result(home_score, away_score, is_independiente_home)
            }
            matches.append(match)
    
    i += 1

print(f"Found {len(matches)} matches")
for m in matches[:5]:
    print(m)

# Save to JSON
with open('/Users/fsodano/fibradev/historia-roja/data/2022_raw.json', 'w', encoding='utf-8') as f:
    json.dump(matches, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(matches)} matches to 2022_raw.json")
