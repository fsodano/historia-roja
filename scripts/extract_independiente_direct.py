#!/usr/bin/env python3
"""
Extract all Independiente matches from the blog using Playwright
"""
import json
import csv
import re

# All the match data extracted from the blog
all_matches = []

# Page 1 data - Copa Sudamericana 2017 and B Nacional 2013/14
page1_matches = [
    # Copa Sudamericana 2017 - Final
    {"date": "06/12/2017", "competition": "Copa Sudamericana 2017 - Final", "match_line": "06/12/2017 en Avellaneda: Independiente de Argentina 2 (Emanuel Gigliotti y Maximiliano Meza), Flamengo de Brasil 1 (Réver)"},
    {"date": "13/12/2017", "competition": "Copa Sudamericana 2017 - Final", "match_line": "13/12/2017 en Río de Janeiro: Flamengo de Brasil 1 (Lucas Paquetá), Independiente de Argentina 1 (Ezequiel Barco)"},
    
    # Copa Sudamericana 2017 - Semifinales  
    {"date": "21/11/2017", "competition": "Copa Sudamericana 2017 - Semifinales", "match_line": "21/11/2017 en Asunción: Libertad de Paraguay 1 (Óscar R. Cardozo), Independiente de Argentina 0"},
    {"date": "28/11/2017", "competition": "Copa Sudamericana 2017 - Semifinales", "match_line": "28/11/2017 en Avellaneda: Independiente de Argentina 3 (Esequiel Barco (p) y Emmanuel Gigliotti 2), Libertad de Paraguay 1 (Ángel R. Cardozo)"},
    
    # B Nacional 2013/14 - only Independiente matches
    {"date": "03/08/2013", "competition": "Primera B Nacional 2013/14", "match_line": "03/08/2013 en Avellaneda: Independiente 1 (Daniel Montenegro (p)), Brown 2 (Martín Fabro y Matías Sproat)"},
    {"date": "11/08/2013", "competition": "Primera B Nacional 2013/14", "match_line": "11/08/2013 en San Francisco: Gimnasia y Esgrima de Jujuy 0, Independiente 2 (Martín Gómez y Fernando Godoy)"},
    {"date": "17/08/2013", "competition": "Primera B Nacional 2013/14", "match_line": "17/08/2013 en Avellaneda: Independiente 3 (Daniel Montenegro, Diego Vera y Cristian Báez), Instituto de Córdoba 1 (Diego A. Suárez)"},
    {"date": "25/08/2013", "competition": "Primera B Nacional 2013/14", "match_line": "25/08/2013 en Paraná: Patronato de Paraná 0, Independiente 1 (Diego Vera)"},
    {"date": "01/09/2013", "competition": "Primera B Nacional 2013/14", "match_line": "01/09/2013 en Avellaneda: Independiente 0, Talleres de Córdoba 0"},
    {"date": "07/09/2013", "competition": "Primera B Nacional 2013/14", "match_line": "07/09/2013 en San Carlos de Bariloche: Cipolletti 1 (Juan F. Ríos), Independiente 1 (Daniel Montenegro)"},
    {"date": "14/09/2013", "competition": "Primera B Nacional 2013/14", "match_line": "14/09/2013 en Avellaneda: Independiente 2 (Jesús Méndez y Juan L. Cavallaro), Aldosivi de Mar del Plata 0"},
    {"date": "21/09/2013", "competition": "Primera B Nacional 2013/14", "match_line": "21/09/2013 en Mendoza: Gimnasia y Esgrima de Mendoza 0, Independiente 2 (Jesús Méndez 2)"},
    {"date": "29/09/2013", "competition": "Primera B Nacional 2013/14", "match_line": "29/09/2013 en Avellaneda: Independiente 0, Ferro Carril Oeste 0"},
]

# Page 2 - Copa Sudamericana 2015 and more
page2_matches = [
    # Copa Sudamericana 2015
    {"date": "26/08/2015", "competition": "Copa Sudamericana 2015", "match_line": "26/08/2015 en Sarandí: Arsenal FC de Argentina 1 (Federico Lértora), Independiente de Argentina 1 (Julián Vitale)"},
    {"date": "16/09/2015", "competition": "Copa Sudamericana 2015", "match_line": "16/09/2015 en Avellaneda: Independiente de Argentina 1 (Lucas Albertengo), Arsenal FC de Argentina 0"},
    {"date": "23/09/2015", "competition": "Copa Sudamericana 2015", "match_line": "23/09/2015 en Avellaneda: Independiente de Argentina 1 (Juan M. Trejo), Olimpia de Paraguay 0"},
    {"date": "30/09/2015", "competition": "Copa Sudamericana 2015", "match_line": "30/09/2015 en Asunción: Olimpia de Paraguay 0, Independiente de Argentina 0"},
    {"date": "22/10/2015", "competition": "Copa Sudamericana 2015", "match_line": "22/10/2015 en Avellaneda: Independiente de Argentina 0, Independiente Santa Fe de Colombia 1 (Leyvin Balanta)"},
    {"date": "29/10/2015", "competition": "Copa Sudamericana 2015", "match_line": "29/10/2015 en Bogotá: Independiente Santa Fe de Colombia 1 (Francisco Meza), Independiente de Argentina 1 (Robinson Zapata e/c)"},
    
    # Copa Sudamericana 2016
    {"date": "25/08/2016", "competition": "Copa Sudamericana 2016", "match_line": "25/08/2016 en Lanús: Lanús de Argentina 0, Independiente de Argentina 2 (Leandro M. Fernández y Emiliano Rigoni)"},
    {"date": "14/09/2016", "competition": "Copa Sudamericana 2016", "match_line": "14/09/2016 en Avellaneda: Independiente de Argentina 1 (Martín Benítez), Lanús de Argentina 0"},
    {"date": "21/09/2016", "competition": "Copa Sudamericana 2016", "match_line": "21/09/2016 en Avellaneda: Independiente de Argentina 0, Chapecoense de Brasil 0"},
    {"date": "28/09/2016", "competition": "Copa Sudamericana 2016", "match_line": "28/09/2016 en Chapecó: Chapecoense de Brasil 0, Independiente de Avellaneda 0"},
    
    # Copa Sudamericana 2017 - earlier rounds
    {"date": "04/04/2017", "competition": "Copa Sudamericana 2017", "match_line": "04/04/2017 en Avellaneda: Independiente de Argentina 0, Alianza Lima de Perú 0"},
    {"date": "31/05/2017", "competition": "Copa Sudamericana 2017", "match_line": "31/05/2017 en Lima: Alianza Lima de Perú 0, Independiente de Argentina 1 (Emiliano A. Rigoni)"},
    {"date": "12/07/2017", "competition": "Copa Sudamericana 2017", "match_line": "12/07/2017 en Avellaneda: Independiente de Argentina 4 (Alan J. Franco, Esequiel O. Barco, Leandro M. Fernández y Nery Domínguez), Deportes Iquique de Chile 2 (Diego O. Bielkiewicz (p) y Leonardo A. Esperanza)"},
    {"date": "02/08/2017", "competition": "Copa Sudamericana 2017", "match_line": "02/08/2017 en Calama: Deportes Iquique de Chile 1 (Manuel A. Villalobos), Independiente de Argentina 2 (Maximiliano E. Meza y Lucas Albertengo)"},
    {"date": "22/08/2017", "competition": "Copa Sudamericana 2017", "match_line": "22/08/2017 en San Miguel de Tucumán: Atlético Tucumán de Tucumán 1 (Luis M. Rodríguez), Independiente de Argentina 0"},
    {"date": "12/09/2017", "competition": "Copa Sudamericana 2017", "match_line": "12/09/2017 en Avellaneda: Independiente de Argentina 2 (Leandro M. Fernández y Martín N. Benítez), Atlético Tucumán de Argentina 0"},
    {"date": "25/10/2017", "competition": "Copa Sudamericana 2017", "match_line": "25/10/2017 en Asunción: Nacional de Paraguay 1 (Luis N. Caballero), Independiente de Argentina 4 (Maximiliano E. Meza, Leandro M. Fernández 2 y Lucas Albertengo)"},
    {"date": "02/11/2017", "competition": "Copa Sudamericana 2017", "match_line": "02/11/2017 en Avellaneda: Independiente de Argentina 2 (Juan M. Martínez y Emmanuel Gigliotti), Nacional de Paraguay 0"},
]

# Combine all matches
all_match_lines = page1_matches + page2_matches

def parse_match_line(match_data):
    """Parse a match line and extract structured data"""
    line = match_data['match_line']
    competition = match_data['competition']
    
    # Pattern: DD/MM/YYYY en location: Team1 score1 (scorers), Team2 score2 (scorers)
    # Handle various formats
    pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d(]+?)\s+(\d+)\s*(?:\([^)]*\))?\s*,\s*([^\d(]+?)\s+(\d+)\s*(?:\([^)]*\))?\s*$'
    
    m = re.search(pattern, line)
    if not m:
        return None
    
    date, location, team1_raw, score1, team2_raw, score2 = m.groups()
    
    team1 = team1_raw.strip()
    team2 = team2_raw.strip()
    
    # Determine if Independiente is involved and which team they are
    t1_lower = team1.lower()
    t2_lower = team2.lower()
    
    is_inde1 = 'independiente' in t1_lower and 'santa fe' not in t1_lower and 'colombia' not in t1_lower
    is_inde2 = 'independiente' in t2_lower and 'santa fe' not in t2_lower and 'colombia' not in t2_lower
    
    if not is_inde1 and not is_inde2:
        return None
    
    try:
        s1, s2 = int(score1), int(score2)
        
        if is_inde1:  # Independiente is team1 (home)
            if s1 > s2:
                result = "WIN"
            elif s1 < s2:
                result = "LOSS"
            else:
                result = "DRAW"
        else:  # Independiente is team2 (away)
            if s2 > s1:
                result = "WIN"
            elif s2 < s1:
                result = "LOSS"
            else:
                result = "DRAW"
        
        return {
            'date': date,
            'competition': competition,
            'home_team': team1,
            'away_team': team2,
            'home_score': score1,
            'away_score': score2,
            'result': result
        }
    except:
        return None

# Parse all matches
parsed_matches = []
for match_data in all_match_lines:
    parsed = parse_match_line(match_data)
    if parsed:
        parsed_matches.append(parsed)

print(f"Parsed {len(parsed_matches)} matches")

# Save to CSV
with open('independiente_matches_extracted.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
    writer.writeheader()
    writer.writerows(parsed_matches)

print(f"Saved to independiente_matches_extracted.csv")

# Print sample
print("\nSample matches:")
for m in parsed_matches[:5]:
    print(f"  {m['date']}: {m['home_team']} {m['home_score']}-{m['away_score']} {m['away_team']} ({m['result']})")
