import json
import re

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

# Filter out non-match lines
lines = [l.strip() for l in text.split('\n') if l.strip()]
matches = []
current_date = None

i = 0
while i < len(lines):
    line = lines[i]
    
    # Check for date line
    date_match = re.match(r'^(Dom\.|Lun\.|Mar\.|Mié\.|Jue\.|Vie\.|Sáb\.)[,\.\s]+(\d+)\s+de\s+(\w+)\.?$', line)
    if date_match:
        day = date_match.group(2).zfill(2)
        month = date_match.group(3).lower()[:3]
        month_num = months_es.get(month, '01')
        current_date = f"{day}/{month_num}/2022"
        i += 1
        continue
    
    # Check for score pattern
    score_match = re.match(r'^(\d+)\s*-\s*(\d+)$', line)
    if score_match and current_date and i >= 2:
        home_score = score_match.group(1)
        away_score = score_match.group(2)
        
        # Find home team (should be before the score)
        home_team = lines[i-1] if i > 0 else ''
        # Find away team (should be after the score)
        away_team = lines[i+1] if i+1 < len(lines) else ''
        
        # Skip penalty shootout info lines
        if 'ganó' in away_team.lower() and 'penales' in away_team.lower():
            # This is a penalty info line, find the actual away team
            away_team = lines[i+2] if i+2 < len(lines) else ''
        
        # Find competition
        competition = 'Liga Profesional de Fútbol'
        for j in range(i+1, min(i+6, len(lines))):
            comp_line = lines[j]
            if 'Finalizado' in comp_line or 'Final' in comp_line:
                # Extract competition from this line
                if '\t' in comp_line:
                    parts = comp_line.split('\t')
                    if len(parts) > 1:
                        competition = parts[-1].strip()
                else:
                    # Try to extract after "Finalizado" or "Final"
                    comp_clean = comp_line.replace('Finalizado', '').replace('Final', '').replace('-', '').replace('Pen', '').strip()
                    if comp_clean and len(comp_clean) > 3:
                        competition = comp_clean
                break
        
        # Determine if Independiente is home
        is_independiente_home = 'Independiente' in home_team
        
        # Only add if this looks like a real match (has both teams and valid score)
        if home_team and away_team and home_team != away_team:
            match = {
                'date': current_date,
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
    print(f"{m['date']}: {m['home_team']} {m['home_score']}-{m['away_score']} {m['away_team']} ({m['result']})")

# Save to JSON
with open('/Users/fsodano/fibradev/historia-roja/data/2022_raw.json', 'w', encoding='utf-8') as f:
    json.dump(matches, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(matches)} matches to 2022_raw.json")
