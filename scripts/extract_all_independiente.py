#!/usr/bin/env python3
"""
Extract all Independiente de Avellaneda matches from josecarluccio.blogspot.com
Data was extracted from the 'independiente' tag pages
"""
import csv
import re
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# All match data extracted from the blog via Playwright
# Format: date, competition, match_line
all_match_lines = [
    # Page 1: Copa Sudamericana 2017 and B Nacional 2013/14
    ("06/12/2017", "Copa Sudamericana 2017 - Final", "06/12/2017 en Avellaneda: Independiente de Argentina 2 (Emanuel Gigliotti y Maximiliano Meza), Flamengo de Brasil 1 (Réver)"),
    ("13/12/2017", "Copa Sudamericana 2017 - Final", "13/12/2017 en Río de Janeiro: Flamengo de Brasil 1 (Lucas Paquetá), Independiente de Argentina 1 (Ezequiel Barco)"),
    ("21/11/2017", "Copa Sudamericana 2017 - Semifinales", "21/11/2017 en Asunción: Libertad de Paraguay 1 (Óscar R. Cardozo), Independiente de Argentina 0"),
    ("28/11/2017", "Copa Sudamericana 2017 - Semifinales", "28/11/2017 en Avellaneda: Independiente de Argentina 3 (Esequiel Barco (p) y Emmanuel Gigliotti 2), Libertad de Paraguay 1 (Ángel R. Cardozo)"),
    
    # B Nacional 2013/14
    ("03/08/2013", "Primera B Nacional 2013/14", "03/08/2013 en Avellaneda: Independiente 1 (Daniel Montenegro (p)), Brown 2 (Martín Fabro y Matías Sproat)"),
    ("11/08/2013", "Primera B Nacional 2013/14", "11/08/2013 en San Francisco: Gimnasia y Esgrima de Jujuy 0, Independiente 2 (Martín Gómez y Fernando Godoy)"),
    ("17/08/2013", "Primera B Nacional 2013/14", "17/08/2013 en Avellaneda: Independiente 3 (Daniel Montenegro, Diego Vera y Cristian Báez), Instituto de Córdoba 1 (Diego A. Suárez)"),
    ("25/08/2013", "Primera B Nacional 2013/14", "25/08/2013 en Paraná: Patronato de Paraná 0, Independiente 1 (Diego Vera)"),
    ("01/09/2013", "Primera B Nacional 2013/14", "01/09/2013 en Avellaneda: Independiente 0, Talleres de Córdoba 0"),
    ("07/09/2013", "Primera B Nacional 2013/14", "07/09/2013 en San Carlos de Bariloche: Cipolletti 1 (Juan F. Ríos), Independiente 1 (Daniel Montenegro)"),
    ("14/09/2013", "Primera B Nacional 2013/14", "14/09/2013 en Avellaneda: Independiente 2 (Jesús Méndez y Juan L. Cavallaro), Aldosivi de Mar del Plata 0"),
    ("21/09/2013", "Primera B Nacional 2013/14", "21/09/2013 en Mendoza: Gimnasia y Esgrima de Mendoza 0, Independiente 2 (Jesús Méndez 2)"),
    ("29/09/2013", "Primera B Nacional 2013/14", "29/09/2013 en Avellaneda: Independiente 0, Ferro Carril Oeste 0"),
    
    # Page 2: Copa Sudamericana 2015, 2016, 2017
    ("26/08/2015", "Copa Sudamericana 2015", "26/08/2015 en Sarandí: Arsenal FC de Argentina 1 (Federico Lértora), Independiente de Argentina 1 (Julián Vitale)"),
    ("16/09/2015", "Copa Sudamericana 2015", "16/09/2015 en Avellaneda: Independiente de Argentina 1 (Lucas Albertengo), Arsenal FC de Argentina 0"),
    ("23/09/2015", "Copa Sudamericana 2015", "23/09/2015 en Avellaneda: Independiente de Argentina 1 (Juan M. Trejo), Olimpia de Paraguay 0"),
    ("30/09/2015", "Copa Sudamericana 2015", "30/09/2015 en Asunción: Olimpia de Paraguay 0, Independiente de Argentina 0"),
    ("22/10/2015", "Copa Sudamericana 2015", "22/10/2015 en Avellaneda: Independiente de Argentina 0, Independiente Santa Fe de Colombia 1 (Leyvin Balanta)"),
    ("29/10/2015", "Copa Sudamericana 2015", "29/10/2015 en Bogotá: Independiente Santa Fe de Colombia 1 (Francisco Meza), Independiente de Argentina 1 (Robinson Zapata e/c)"),
    ("25/08/2016", "Copa Sudamericana 2016", "25/08/2016 en Lanús: Lanús de Argentina 0, Independiente de Argentina 2 (Leandro M. Fernández y Emiliano Rigoni)"),
    ("14/09/2016", "Copa Sudamericana 2016", "14/09/2016 en Avellaneda: Independiente de Argentina 1 (Martín Benítez), Lanús de Argentina 0"),
    ("21/09/2016", "Copa Sudamericana 2016", "21/09/2016 en Avellaneda: Independiente de Argentina 0, Chapecoense de Brasil 0"),
    ("28/09/2016", "Copa Sudamericana 2016", "28/09/2016 en Chapecó: Chapecoense de Brasil 0, Independiente de Avellaneda 0"),
    ("04/04/2017", "Copa Sudamericana 2017", "04/04/2017 en Avellaneda: Independiente de Argentina 0, Alianza Lima de Perú 0"),
    ("31/05/2017", "Copa Sudamericana 2017", "31/05/2017 en Lima: Alianza Lima de Perú 0, Independiente de Argentina 1 (Emiliano A. Rigoni)"),
    ("12/07/2017", "Copa Sudamericana 2017", "12/07/2017 en Avellaneda: Independiente de Argentina 4 (Alan J. Franco, Esequiel O. Barco, Leandro M. Fernández y Nery Domínguez), Deportes Iquique de Chile 2 (Diego O. Bielkiewicz (p) y Leonardo A. Esperanza)"),
    ("02/08/2017", "Copa Sudamericana 2017", "02/08/2017 en Calama: Deportes Iquique de Chile 1 (Manuel A. Villalobos), Independiente de Argentina 2 (Maximiliano E. Meza y Lucas Albertengo)"),
    ("22/08/2017", "Copa Sudamericana 2017", "22/08/2017 en San Miguel de Tucumán: Atlético Tucumán de Tucumán 1 (Luis M. Rodríguez), Independiente de Argentina 0"),
    ("12/09/2017", "Copa Sudamericana 2017", "12/09/2017 en Avellaneda: Independiente de Argentina 2 (Leandro M. Fernández y Martín N. Benítez), Atlético Tucumán de Argentina 0"),
    ("25/10/2017", "Copa Sudamericana 2017", "25/10/2017 en Asunción: Nacional de Paraguay 1 (Luis N. Caballero), Independiente de Argentina 4 (Maximiliano E. Meza, Leandro M. Fernández 2 y Lucas Albertengo)"),
    ("02/11/2017", "Copa Sudamericana 2017", "02/11/2017 en Avellaneda: Independiente de Argentina 2 (Juan M. Martínez y Emmanuel Gigliotti), Nacional de Paraguay 0"),
    
    # Copa Sudamericana 2010
    ("26/08/2010", "Copa Sudamericana 2010", "26/08/2010 en Avellaneda: Independiente 1 (Leonel Galeano), Argentinos Juniors 0"),
    ("09/09/2010", "Copa Sudamericana 2010", "09/09/2010 en Buenos Aires: Argentinos Juniors 1 (Néstor Ortigoza (p)), Independiente 1 (Leandro Gracián)"),
    ("28/09/2010", "Copa Sudamericana 2010", "28/09/2010 en Montevideo: Defensor Sporting 1 (Leandro Gracián e/c), Independiente 0"),
    ("19/10/2010", "Copa Sudamericana 2010", "19/10/2010 en Avellaneda: Independiente 4 (Andrés Silvera, Hernán Fredes, Nicolás Cabrera y Nicolás Martínez), Defensor Sporting 2 (Rodrigo Mora y Diego Rodríguez)"),
    ("03/11/2010", "Copa Sudamericana 2010", "03/11/2010 en Ibagué: Deportes Tolima 2 (Wilder Medina y Rodrigo Marangoni), Independiente 2 (Andrés Silvera (p) y Julián Velázquez)"),
    ("11/11/2010", "Copa Sudamericana 2010", "11/11/2010 en Avellaneda: Independiente 0, Deportes Tolima 0"),
    ("18/11/2010", "Copa Sudamericana 2010", "18/11/2010 en Quito: Liga Deportiva Universitaria 3 (Juan M. Salgueiro, Miller Bolaños y Néicer Reasco), Independiente 2 (Andrés Silvera y Lucas Mareque)"),
    ("25/11/2010", "Copa Sudamericana 2010", "25/11/2010 en Avellaneda: Independiente 2 (Facundo Parra y Hernán Fredes), Liga Deportiva Universitaria 1 (Juan M. Salgueiro)"),
    ("01/12/2010", "Copa Sudamericana 2010", "01/12/2010 en Goiania: Goiás 2 (Rafael Moura y Otacílio Neto), Independiente 0"),
    ("08/12/2010", "Copa Sudamericana 2010", "08/12/2010 en Avellaneda: Independiente 3 (Julián Velázquez y Facundo Parra 2), Goiás 1 (Rafael Moura)"),
    
    # Copa Sudamericana 2011-2012
    ("28/09/2011", "Copa Sudamericana 2011", "28/09/2011 en Quito: Liga Deportiva Universitaria 2 (Paul V. Ambrossi y Luis A. Bolaños León), Independiente 0"),
    ("12/10/2011", "Copa Sudamericana 2011", "12/10/2011 en Avellaneda: Independiente 1 (Leonel J. Núñez), Liga Deportiva Universitaria 0"),
    ("22/08/2012", "Copa Sudamericana 2012", "22/08/2012 en Buenos Aires: Boca Juniors 3 (Santiago Silva, Leandro Somoza y Juan Sánchez Miño), Independiente 3 (Jonathan Santana, Paulo Rosales y Ernesto Farías)"),
    ("29/08/2012", "Copa Sudamericana 2012", "29/08/2012 en Avellaneda: Independiente 0, Boca Juniors 0"),
    ("25/09/2012", "Copa Sudamericana 2012", "25/09/2012 en Avellaneda: Independiente 2 (Fabián Vargas y Paulo Rosales), Liverpool 1 (Carlos Núñez)"),
    ("25/10/2012", "Copa Sudamericana 2012", "25/10/2012 en Montevideo: Liverpool 1 (Carlos Núñez), Independiente 2 (Federico Mancuello y Roberto Battión)"),
    ("01/11/2012", "Copa Sudamericana 2012", "01/11/2012 en Avellaneda: Independiente 2 (Cristian Tula y Hans Martínez), Universidad Católica 2 (Enzo Andía y Nicolás Castillo)"),
    ("08/11/2012", "Copa Sudamericana 2012", "08/11/2012 en Santiago: Universidad Católica 2 (Michael Ríos 2 (2p)), Independiente 1 (Jonathan Santana)"),
    
    # Recopa Sudamericana 2011
    ("10/08/2011", "Recopa Sudamericana 2011", "10/08/2011 en Avellaneda: Independiente de Argentina 2 (Maximiliano Velázquez y Marco Pérez), Internacional 1 (Leandro Damiao)"),
    ("24/08/2011", "Recopa Sudamericana 2011", "24/08/2011 en Porto Alegre: Internacional de Brasil 3 (Leandro Damiao 2 y Kléber (p)), Independiente 1 (Maximiliano Velázquez)"),
    
    # Copa Libertadores 2011
    ("25/01/2011", "Copa Libertadores 2011", "25/01/2011 en Avellaneda: Independiente 2 (Matías Defederico y Patricio Rodríguez), Deportivo Quito 0"),
    ("01/02/2011", "Copa Libertadores 2011", "01/02/2011 en Quito: Deportivo Quito 1 (Michael Quiñónez), Independiente 0"),
    ("24/02/2011", "Copa Libertadores 2011", "24/02/2011 en Avellaneda: Independiente 3 (Facundo Parra, Cristian Pellerano y Andrés Silvera), Peñarol 0"),
    ("03/03/2011", "Copa Libertadores 2011", "03/03/2011 en Quito: Liga Deportiva Universitaria 3 (Paul Ambrossi, Miller Bolaños y Patricio Urrutia), Independiente 0"),
    ("10/03/2011", "Copa Libertadores 2011", "10/03/2011 en Avellaneda: Independiente 1 (Facundo Parra), Godoy Cruz Antonio Tomba 3 (Hernán Fredes e/c, Ariel Rojas y Rubén Ramírez)"),
    ("22/03/2011", "Copa Libertadores 2011", "22/03/2011 en Mendoza: Godoy Cruz Antonio Tomba 1 (Rubén Ramírez), Independiente 1 (Matías Defederico)"),
    ("05/04/2011", "Copa Libertadores 2011", "05/04/2011 en Avellaneda: Independiente 1 (Leonel Núñez), Liga Deportiva Universitaria 1 (Julián Velázquez e/c)"),
    ("12/04/2011", "Copa Libertadores 2011", "12/04/2011 en Montevideo: Peñarol 0, Independiente 1 (Facundo Parra)"),
]

def parse_match_line(date, competition, line):
    """Parse a match line and extract structured data"""
    # Pattern: DD/MM/YYYY en location: Team1 score1 (scorers), Team2 score2 (scorers)
    pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s*([^\d(]+?)\s+(\d+)\s*(?:\([^)]*\))?\s*,\s*([^\d(]+?)\s+(\d+)\s*(?:\([^)]*\))?\s*$'
    
    m = re.search(pattern, line)
    if not m:
        return None
    
    _, _, team1_raw, score1, team2_raw, score2 = m.groups()
    
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
        
        if is_inde1:
            result = "WIN" if s1 > s2 else "LOSS" if s1 < s2 else "DRAW"
        else:
            result = "WIN" if s2 > s1 else "LOSS" if s2 < s1 else "DRAW"
        
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

def main():
    print("=" * 60)
    print("Extracting Independiente de Avellaneda Matches")
    print("=" * 60)
    print()
    
    # Parse all matches
    parsed_matches = []
    for date, competition, line in all_match_lines:
        parsed = parse_match_line(date, competition, line)
        if parsed:
            parsed_matches.append(parsed)
    
    print(f"Total matches extracted: {len(parsed_matches)}")
    print()
    
    # Group by year
    matches_by_year = {}
    for m in parsed_matches:
        year = m['date'].split('/')[-1]
        if year not in matches_by_year:
            matches_by_year[year] = []
        matches_by_year[year].append(m)
    
    # Save to CSV files by year
    print("Saving matches by year...")
    for year in sorted(matches_by_year.keys()):
        year_matches = matches_by_year[year]
        filename = os.path.join(DATA_DIR, f"{year}.csv")
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
            writer.writeheader()
            writer.writerows(year_matches)
        
        print(f"  {year}: {len(year_matches)} matches -> {filename}")
    
    # Save combined file
    combined_file = "independiente_matches_all.csv"
    with open(combined_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        writer.writeheader()
        writer.writerows(parsed_matches)
    
    print(f"\nCombined file: {combined_file} ({len(parsed_matches)} matches)")
    print()
    
    # Print summary
    print("Summary by competition:")
    comp_counts = {}
    for m in parsed_matches:
        comp = m['competition']
        comp_counts[comp] = comp_counts.get(comp, 0) + 1
    
    for comp, count in sorted(comp_counts.items(), key=lambda x: -x[1]):
        print(f"  {comp}: {count} matches")
    
    print()
    print("Sample matches:")
    for m in parsed_matches[:5]:
        print(f"  {m['date']}: {m['home_team']} {m['home_score']}-{m['away_score']} {m['away_team']} ({m['result']})")

if __name__ == "__main__":
    main()
