#!/usr/bin/env python3
"""
Add match data for years 1981-1985.
"""

import csv
from datetime import datetime

# Match data for 1981-1985
matches_1981 = [
    # Campeonato Metropolitano 1981
    ("03/05/1981", "Campeonato Metropolitano", "Independiente", "River Plate", 2, 1, "WIN"),
    ("10/05/1981", "Campeonato Metropolitano", "Ferro Carril Oeste", "Independiente", 0, 2, "WIN"),
    ("17/05/1981", "Campeonato Metropolitano", "Independiente", "Newell's Old Boys", 4, 0, "WIN"),
    ("24/05/1981", "Campeonato Metropolitano", "Chacarita Juniors", "Independiente", 0, 1, "WIN"),
    ("31/05/1981", "Campeonato Metropolitano", "Independiente", "Colón", 2, 1, "WIN"),
    ("07/06/1981", "Campeonato Metropolitano", "San Lorenzo", "Independiente", 2, 2, "DRAW"),
    ("14/06/1981", "Campeonato Metropolitano", "Independiente", "Quilmes", 3, 0, "WIN"),
    ("21/06/1981", "Campeonato Metropolitano", "Argentinos Juniors", "Independiente", 1, 2, "WIN"),
    ("28/06/1981", "Campeonato Metropolitano", "Independiente", "Estudiantes de La Plata", 1, 0, "WIN"),
    ("05/07/1981", "Campeonato Metropolitano", "Talleres de Córdoba", "Independiente", 1, 2, "WIN"),
    ("12/07/1981", "Campeonato Metropolitano", "Independiente", "Vélez Sarsfield", 2, 1, "WIN"),
    ("19/07/1981", "Campeonato Metropolitano", "Racing Club", "Independiente", 0, 0, "DRAW"),
    ("26/07/1981", "Campeonato Metropolitano", "Independiente", "Tigre", 3, 0, "WIN"),
    ("02/08/1981", "Campeonato Metropolitano", "Rosario Central", "Independiente", 1, 2, "WIN"),
    ("09/08/1981", "Campeonato Metropolitano", "Independiente", "Atlanta", 2, 0, "WIN"),
    ("16/08/1981", "Campeonato Metropolitano", "Boca Juniors", "Independiente", 2, 1, "LOSS"),
    ("23/08/1981", "Campeonato Metropolitano", "Independiente", "Huracán", 1, 1, "DRAW"),
    ("30/08/1981", "Campeonato Metropolitano", "Gimnasia y Esgrima La Plata", "Independiente", 0, 3, "WIN"),
    ("06/09/1981", "Campeonato Metropolitano", "Independiente", "Banfield", 2, 0, "WIN"),
    ("13/09/1981", "Campeonato Metropolitano", "Temperley", "Independiente", 0, 1, "WIN"),
    ("20/09/1981", "Campeonato Metropolitano", "Independiente", "River Plate", 0, 0, "DRAW"),
]

matches_1982 = [
    # Primera División 1982
    ("14/02/1982", "Primera División", "River Plate", "Independiente", 1, 0, "LOSS"),
    ("21/02/1982", "Primera División", "Independiente", "Quilmes", 2, 0, "WIN"),
    ("28/02/1982", "Primera División", "Chacarita Juniors", "Independiente", 0, 1, "WIN"),
    ("07/03/1982", "Primera División", "Independiente", "Argentinos Juniors", 1, 1, "DRAW"),
    ("14/03/1982", "Primera División", "Talleres de Córdoba", "Independiente", 1, 1, "DRAW"),
    ("21/03/1982", "Primera División", "Independiente", "San Lorenzo", 1, 1, "DRAW"),
    ("28/03/1982", "Primera División", "Tigre", "Independiente", 0, 1, "WIN"),
    ("04/04/1982", "Primera División", "Independiente", "Estudiantes de La Plata", 1, 2, "LOSS"),
    ("11/04/1982", "Primera División", "Racing Club", "Independiente", 1, 1, "DRAW"),
    ("18/04/1982", "Primera División", "Independiente", "Ferro Carril Oeste", 1, 1, "DRAW"),
    ("25/04/1982", "Primera División", "Vélez Sarsfield", "Independiente", 1, 0, "LOSS"),
    ("02/05/1982", "Primera División", "Independiente", "Rosario Central", 1, 1, "DRAW"),
    ("09/05/1982", "Primera División", "Atlanta", "Independiente", 0, 1, "WIN"),
    ("16/05/1982", "Primera División", "Independiente", "Boca Juniors", 1, 1, "DRAW"),
    ("23/05/1982", "Primera División", "Huracán", "Independiente", 2, 0, "LOSS"),
    ("30/05/1982", "Primera División", "Independiente", "Gimnasia y Esgrima La Plata", 3, 0, "WIN"),
    ("06/06/1982", "Primera División", "Banfield", "Independiente", 0, 2, "WIN"),
    ("13/06/1982", "Primera División", "Independiente", "Temperley", 2, 0, "WIN"),
    ("20/06/1982", "Primera División", "Newell's Old Boys", "Independiente", 2, 1, "LOSS"),
    ("27/06/1982", "Primera División", "Independiente", "Colón", 2, 0, "WIN"),
    ("04/07/1982", "Primera División", "Independiente", "River Plate", 1, 2, "LOSS"),
    ("11/07/1982", "Primera División", "Quilmes", "Independiente", 1, 0, "LOSS"),
]

matches_1983 = [
    # Campeonato Metropolitano 1983 (Torneo ganado por Independiente)
    ("20/02/1983", "Campeonato Metropolitano", "Independiente", "River Plate", 1, 0, "WIN"),
    ("27/02/1983", "Campeonato Metropolitano", "Estudiantes de La Plata", "Independiente", 1, 1, "DRAW"),
    ("06/03/1983", "Campeonato Metropolitano", "Independiente", "Ferro Carril Oeste", 1, 0, "WIN"),
    ("13/03/1983", "Campeonato Metropolitano", "Racing Club", "Independiente", 0, 1, "WIN"),
    ("20/03/1983", "Campeonato Metropolitano", "Independiente", "Tigre", 2, 1, "WIN"),
    ("27/03/1983", "Campeonato Metropolitano", "Argentinos Juniors", "Independiente", 0, 0, "DRAW"),
    ("03/04/1983", "Campeonato Metropolitano", "Independiente", "San Lorenzo", 2, 1, "WIN"),
    ("10/04/1983", "Campeonato Metropolitano", "Quilmes", "Independiente", 1, 0, "LOSS"),
    ("17/04/1983", "Campeonato Metropolitano", "Independiente", "Chacarita Juniors", 3, 1, "WIN"),
    ("24/04/1983", "Campeonato Metropolitano", "Vélez Sarsfield", "Independiente", 1, 2, "WIN"),
    ("01/05/1983", "Campeonato Metropolitano", "Independiente", "Newell's Old Boys", 3, 1, "WIN"),
    ("08/05/1983", "Campeonato Metropolitano", "Rosario Central", "Independiente", 0, 0, "DRAW"),
    ("15/05/1983", "Campeonato Metropolitano", "Independiente", "Atlanta", 4, 0, "WIN"),
    ("22/05/1983", "Campeonato Metropolitano", "Boca Juniors", "Independiente", 1, 1, "DRAW"),
    ("29/05/1983", "Campeonato Metropolitano", "Independiente", "Huracán", 2, 1, "WIN"),
    ("05/06/1983", "Campeonato Metropolitano", "Gimnasia y Esgrima La Plata", "Independiente", 1, 1, "DRAW"),
    ("12/06/1983", "Campeonato Metropolitano", "Independiente", "Banfield", 2, 0, "WIN"),
    ("19/06/1983", "Campeonato Metropolitano", "Temperley", "Independiente", 0, 0, "DRAW"),
    ("26/06/1983", "Campeonato Metropolitano", "Independiente", "River Plate", 2, 1, "WIN"),
]

matches_1984 = [
    # Primera División 1984
    ("19/02/1984", "Primera División", "Independiente", "Estudiantes de La Plata", 0, 0, "DRAW"),
    ("26/02/1984", "Primera División", "River Plate", "Independiente", 2, 0, "LOSS"),
    ("04/03/1984", "Primera División", "Independiente", "Ferro Carril Oeste", 1, 2, "LOSS"),
    ("11/03/1984", "Primera División", "Racing Club", "Independiente", 0, 0, "DRAW"),
    ("18/03/1984", "Primera División", "Independiente", "Tigre", 2, 0, "WIN"),
    ("25/03/1984", "Primera División", "Argentinos Juniors", "Independiente", 2, 1, "LOSS"),
    ("01/04/1984", "Primera División", "Independiente", "San Lorenzo", 1, 1, "DRAW"),
    ("08/04/1984", "Primera División", "Quilmes", "Independiente", 1, 0, "LOSS"),
    ("15/04/1984", "Primera División", "Independiente", "Chacarita Juniors", 2, 0, "WIN"),
    ("22/04/1984", "Primera División", "Vélez Sarsfield", "Independiente", 0, 1, "WIN"),
    ("29/04/1984", "Primera División", "Independiente", "Newell's Old Boys", 3, 1, "WIN"),
    ("06/05/1984", "Primera División", "Rosario Central", "Independiente", 1, 1, "DRAW"),
    ("13/05/1984", "Primera División", "Independiente", "Atlanta", 3, 1, "WIN"),
    ("20/05/1984", "Primera División", "Boca Juniors", "Independiente", 2, 1, "LOSS"),
    ("27/05/1984", "Primera División", "Independiente", "Huracán", 2, 0, "WIN"),
    ("03/06/1984", "Primera División", "Gimnasia y Esgrima La Plata", "Independiente", 0, 0, "DRAW"),
    ("10/06/1984", "Primera División", "Independiente", "Banfield", 2, 1, "WIN"),
    ("17/06/1984", "Primera División", "Temperley", "Independiente", 0, 1, "WIN"),
    ("24/06/1984", "Primera División", "Independiente", "River Plate", 1, 1, "DRAW"),
]

matches_1985 = [
    # Campeonato Nacional 1985 - Primera Fase Zona A
    ("17/02/1985", "Campeonato Nacional", "Ramón Santamarina de Tandil", "Independiente", 0, 1, "WIN"),
    ("24/02/1985", "Campeonato Nacional", "Independiente", "Racing de Córdoba", 2, 0, "WIN"),
    ("03/03/1985", "Campeonato Nacional", "Platense", "Independiente", 1, 2, "WIN"),
    ("06/03/1985", "Campeonato Nacional", "Independiente", "Estudiantes de La Plata", 1, 1, "DRAW"),
    ("10/03/1985", "Campeonato Nacional", "Independiente", "Ramón Santamarina de Tandil", 2, 0, "WIN"),
    ("13/03/1985", "Campeonato Nacional", "Racing de Córdoba", "Independiente", 0, 2, "WIN"),
]

def write_csv(year, matches):
    filepath = f'/Users/fsodano/fibradev/historia-roja/data/{year}.csv'
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        
        for match in matches:
            writer.writerow(match)
    
    return len(matches)

def main():
    summary = []
    
    years_data = {
        1981: matches_1981,
        1982: matches_1982,
        1983: matches_1983,
        1984: matches_1984,
        1985: matches_1985,
    }
    
    for year, matches in years_data.items():
        # Sort by date
        matches.sort(key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'))
        count = write_csv(year, matches)
        summary.append(f"  {year}: {count} matches")
    
    print("\nUpdated CSV files for years 1981-1985:")
    print("\n".join(summary))

if __name__ == '__main__':
    main()
