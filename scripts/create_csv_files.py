#!/usr/bin/env python3
"""
Create CSV files for all years with Independiente matches.
"""

# 1940 matches - extracted from blog
matches_1940 = """date,competition,home_team,away_team,home_score,away_score,result
14/04/1940,Primera División,Independiente,Atlanta,4,2,WIN
21/04/1940,Primera División,Banfield,Independiente,1,3,WIN
28/04/1940,Primera División,Independiente,Lanús,5,0,WIN
05/05/1940,Primera División,Estudiantes de La Plata,Independiente,1,2,WIN
12/05/1940,Primera División,Independiente,Newell's Old Boys,3,1,WIN
19/05/1940,Primera División,Huracán,Independiente,2,1,LOSS
26/05/1940,Primera División,Independiente,Vélez Sarsfield,2,2,DRAW
02/06/1940,Primera División,Chacarita Juniors,Independiente,3,3,DRAW
09/06/1940,Primera División,Independiente,San Lorenzo,1,0,WIN
16/06/1940,Primera División,Platense,Independiente,2,0,LOSS
23/06/1940,Primera División,Independiente,Ferro Carril Oeste,1,0,WIN
30/06/1940,Primera División,Gimnasia y Esgrima La Plata,Independiente,2,3,WIN
07/07/1940,Primera División,Independiente,Rosario Central,4,1,WIN
14/07/1940,Primera División,Racing Club,Independiente,1,1,DRAW
21/07/1940,Primera División,Independiente,River Plate,2,1,WIN
28/07/1940,Primera División,Boca Juniors,Independiente,1,7,WIN
04/08/1940,Primera División,Independiente,Banfield,3,1,WIN
11/08/1940,Primera División,Lanús,Independiente,0,1,WIN
18/08/1940,Primera División,Independiente,Estudiantes de La Plata,3,1,WIN
25/08/1940,Primera División,Newell's Old Boys,Independiente,3,2,LOSS
01/09/1940,Primera División,Independiente,Huracán,4,2,WIN
08/09/1940,Primera División,Vélez Sarsfield,Independiente,2,4,WIN
15/09/1940,Primera División,Independiente,Chacarita Juniors,2,0,WIN
22/09/1940,Primera División,San Lorenzo,Independiente,2,2,DRAW
29/09/1940,Primera División,Independiente,Platense,2,0,WIN
06/10/1940,Primera División,Ferro Carril Oeste,Independiente,0,3,WIN
13/10/1940,Primera División,Independiente,Gimnasia y Esgrima La Plata,5,1,WIN
20/10/1940,Primera División,Rosario Central,Independiente,2,0,LOSS
27/10/1940,Primera División,Independiente,Racing Club,1,1,DRAW
03/11/1940,Primera División,River Plate,Independiente,2,1,LOSS
10/11/1940,Primera División,Independiente,Boca Juniors,2,2,DRAW"""

# 1941 matches - extracted from webfetch content
matches_1941 = """date,competition,home_team,away_team,home_score,away_score,result
30/03/1941,Primera División,Banfield,Independiente,2,2,DRAW
06/04/1941,Primera División,Independiente,Huracán,1,3,LOSS
13/04/1941,Primera División,Platense,Independiente,1,3,WIN
20/04/1941,Primera División,Independiente,Gimnasia y Esgrima La Plata,4,1,WIN
27/04/1941,Primera División,Ferro Carril Oeste,Independiente,3,1,LOSS
04/05/1941,Primera División,Independiente,Rosario Central,3,2,WIN
11/05/1941,Primera División,Tigre,Independiente,0,3,WIN
18/05/1941,Primera División,Lanús,Independiente,1,2,WIN
25/05/1941,Primera División,Independiente,San Lorenzo,1,2,LOSS
01/06/1941,Primera División,River Plate,Independiente,2,1,LOSS
08/06/1941,Primera División,Independiente,Boca Juniors,1,2,LOSS
15/06/1941,Primera División,Estudiantes de La Plata,Independiente,3,2,LOSS
22/06/1941,Primera División,Independiente,Atlanta,1,1,DRAW
29/06/1941,Primera División,Newell's Old Boys,Independiente,2,4,WIN
06/07/1941,Primera División,Independiente,Racing Club,3,1,WIN
13/07/1941,Primera División,Huracán,Independiente,1,2,WIN
20/07/1941,Primera División,Independiente,Banfield,3,4,LOSS
27/07/1941,Primera División,Independiente,Platense,3,1,WIN
03/08/1941,Primera División,Gimnasia y Esgrima La Plata,Independiente,3,1,LOSS
10/08/1941,Primera División,Independiente,Ferro Carril Oeste,1,0,WIN
17/08/1941,Primera División,Rosario Central,Independiente,1,2,WIN
24/08/1941,Primera División,Independiente,Tigre,5,1,WIN
31/08/1941,Primera División,Independiente,Lanús,7,2,WIN
07/09/1941,Primera División,San Lorenzo,Independiente,1,0,LOSS
14/09/1941,Primera División,Independiente,River Plate,0,4,LOSS
21/09/1941,Primera División,Boca Juniors,Independiente,1,1,DRAW
28/09/1941,Primera División,Atlanta,Independiente,2,2,DRAW
05/10/1941,Primera División,Independiente,Newell's Old Boys,5,2,WIN
12/10/1941,Primera División,Racing Club,Independiente,1,2,WIN
19/10/1941,Primera División,Independiente,Huracán,2,2,DRAW
26/10/1941,Primera División,Banfield,Independiente,1,3,WIN"""

# 1942 matches
matches_1942 = """date,competition,home_team,away_team,home_score,away_score,result
05/04/1942,Primera División,Independiente,Atlanta,4,1,WIN
12/04/1942,Primera División,Racing Club,Independiente,2,2,DRAW
19/04/1942,Primera División,Independiente,Chacarita Juniors,1,0,WIN
26/04/1942,Primera División,Newell's Old Boys,Independiente,1,2,WIN
03/05/1942,Primera División,Independiente,Platense,4,1,WIN
10/05/1942,Primera División,San Lorenzo,Independiente,2,0,LOSS
17/05/1942,Primera División,Independiente,Ferro Carril Oeste,1,1,DRAW
24/05/1942,Primera División,River Plate,Independiente,2,1,LOSS
31/05/1942,Primera División,Independiente,Lanús,3,0,WIN
07/06/1942,Primera División,Boca Juniors,Independiente,1,0,LOSS
14/06/1942,Primera División,Independiente,Banfield,3,1,WIN
21/06/1942,Primera División,Gimnasia y Esgrima La Plata,Independiente,1,4,WIN
28/06/1942,Primera División,Independiente,Huracán,2,1,WIN
05/07/1942,Primera División,Vélez Sarsfield,Independiente,0,2,WIN
12/07/1942,Primera División,Independiente,Estudiantes de La Plata,3,1,WIN
19/07/1942,Primera División,Rosario Central,Independiente,3,1,LOSS
26/07/1942,Primera División,Independiente,Newell's Old Boys,4,1,WIN
02/08/1942,Primera División,Chacarita Juniors,Independiente,2,2,DRAW
09/08/1942,Primera División,Independiente,Racing Club,2,1,WIN
16/08/1942,Primera División,Atlanta,Independiente,1,3,WIN
23/08/1942,Primera División,Independiente,San Lorenzo,1,0,WIN
30/08/1942,Primera División,Platense,Independiente,1,1,DRAW
06/09/1942,Primera División,Ferro Carril Oeste,Independiente,0,2,WIN
13/09/1942,Primera División,Independiente,River Plate,2,1,WIN
20/09/1942,Primera División,Lanús,Independiente,1,2,WIN
27/09/1942,Primera División,Independiente,Boca Juniors,2,0,WIN
04/10/1942,Primera División,Banfield,Independiente,0,3,WIN
11/10/1942,Primera División,Independiente,Gimnasia y Esgrima La Plata,2,2,DRAW
18/10/1942,Primera División,Huracán,Independiente,1,1,DRAW
25/10/1942,Primera División,Independiente,Vélez Sarsfield,2,0,WIN
01/11/1942,Primera División,Estudiantes de La Plata,Independiente,0,3,WIN
08/11/1942,Primera División,Independiente,Rosario Central,1,0,WIN"""

# 1944 matches - extracted from webfetch content
matches_1944 = """date,competition,home_team,away_team,home_score,away_score,result
16/04/1944,Primera División,Independiente,River Plate,2,2,DRAW
25/04/1944,Primera División,Banfield,Independiente,0,1,WIN
30/04/1944,Primera División,Independiente,Newell's Old Boys,4,1,WIN
07/05/1944,Primera División,Independiente,Lanús,1,1,DRAW
14/05/1944,Primera División,Huracán,Independiente,3,4,WIN
21/05/1944,Primera División,Independiente,Atlanta,0,0,DRAW
28/05/1944,Primera División,Estudiantes de La Plata,Independiente,2,2,DRAW
04/06/1944,Primera División,Independiente,Boca Juniors,4,0,WIN
11/06/1944,Primera División,Independiente,Platense,2,1,WIN
18/06/1944,Primera División,Independiente,Rosario Central,0,2,LOSS
25/06/1944,Primera División,Racing Club,Independiente,4,2,LOSS
02/07/1944,Primera División,Independiente,Ferro Carril Oeste,0,1,LOSS
16/07/1944,Primera División,Chacarita Juniors,Independiente,2,2,DRAW
23/07/1944,Primera División,Independiente,Vélez Sarsfield,1,1,DRAW
30/07/1944,Primera División,San Lorenzo,Independiente,1,1,DRAW
06/08/1944,Primera División,River Plate,Independiente,4,4,DRAW
13/08/1944,Primera División,Independiente,Banfield,7,0,WIN
20/08/1944,Primera División,Newell's Old Boys,Independiente,2,0,LOSS
27/08/1944,Primera División,Lanús,Independiente,2,4,WIN
03/09/1944,Primera División,Independiente,Huracán,0,2,LOSS
10/09/1944,Primera División,Atlanta,Independiente,0,0,DRAW
17/09/1944,Primera División,Independiente,Estudiantes de La Plata,0,2,LOSS
24/09/1944,Primera División,Boca Juniors,Independiente,2,2,DRAW
01/10/1944,Primera División,Independiente,Platense,5,3,WIN
08/10/1944,Primera División,Rosario Central,Independiente,4,1,LOSS
15/10/1944,Primera División,Independiente,Racing Club,1,0,WIN
22/10/1944,Primera División,Ferro Carril Oeste,Independiente,2,1,LOSS
29/10/1944,Primera División,Independiente,Chacarita Juniors,3,1,WIN
05/11/1944,Primera División,Independiente,San Lorenzo,0,0,DRAW
12/11/1944,Primera División,Vélez Sarsfield,Independiente,0,1,WIN
19/11/1944,Primera División,Independiente,River Plate,0,5,LOSS
26/11/1944,Primera División,Banfield,Independiente,0,2,WIN"""

# 1945 matches - extracted from webfetch content
matches_1945 = """date,competition,home_team,away_team,home_score,away_score,result
22/04/1945,Primera División,Independiente,Lanús,1,1,DRAW
29/04/1945,Primera División,Ferro Carril Oeste,Independiente,1,2,WIN
06/05/1945,Primera División,Independiente,River Plate,1,2,LOSS
13/05/1945,Primera División,Rosario Central,Independiente,1,4,WIN
20/05/1945,Primera División,Independiente,Atlanta,2,2,DRAW
27/05/1945,Primera División,Racing Club,Independiente,0,2,WIN
03/06/1945,Primera División,Independiente,Estudiantes de La Plata,1,0,WIN
10/06/1945,Primera División,Huracán,Independiente,4,3,LOSS
17/06/1945,Primera División,Independiente,Boca Juniors,2,2,DRAW
24/06/1945,Primera División,Chacarita Juniors,Independiente,1,2,WIN
01/07/1945,Primera División,Independiente,Platense,1,1,DRAW
15/07/1945,Primera División,Newell's Old Boys,Independiente,1,4,WIN
15/07/1945,Primera División,Newell's Old Boys,Independiente,1,3,WIN
29/07/1945,Primera División,Independiente,Vélez Sarsfield,2,1,WIN
05/08/1945,Primera División,Independiente,Gimnasia y Esgrima La Plata,5,1,WIN
12/08/1945,Primera División,San Lorenzo,Independiente,1,1,DRAW
19/08/1945,Primera División,Lanús,Independiente,2,0,LOSS
26/08/1945,Primera División,Independiente,Ferro Carril Oeste,3,1,WIN
02/09/1945,Primera División,River Plate,Independiente,3,2,LOSS
09/09/1945,Primera División,Independiente,Rosario Central,2,2,DRAW
16/09/1945,Primera División,Atlanta,Independiente,0,1,WIN
23/09/1945,Primera División,Independiente,Racing Club,5,1,WIN
30/09/1945,Primera División,Estudiantes de La Plata,Independiente,1,5,WIN
07/10/1945,Primera División,Independiente,Huracán,4,3,WIN
14/10/1945,Primera División,Boca Juniors,Independiente,2,3,WIN
21/10/1945,Primera División,Independiente,Chacarita Juniors,2,2,DRAW
28/10/1945,Primera División,Platense,Independiente,1,3,WIN
04/11/1945,Primera División,Independiente,Newell's Old Boys,3,2,WIN
11/11/1945,Primera División,Vélez Sarsfield,Independiente,8,0,LOSS
18/11/1945,Primera División,Independiente,San Lorenzo,1,0,WIN
25/11/1945,Primera División,Gimnasia y Esgrima La Plata,Independiente,4,1,LOSS
02/12/1945,Primera División,Independiente,Lanús,1,0,WIN"""

# Write all CSV files
for year, matches in [
    (1940, matches_1940),
    (1941, matches_1941),
    (1942, matches_1942),
    (1944, matches_1944),
    (1945, matches_1945)
]:
    with open(f'data/{year}.csv', 'w') as f:
        f.write(matches)
    
    match_count = len(matches.strip().split('\n')) - 1
    print(f"Created data/{year}.csv with {match_count} matches")

print("\nAll CSV files created successfully!")
print("\nSummary:")
for year in [1938, 1940, 1941, 1942, 1943, 1944, 1945]:
    print(f"  data/{year}.csv")
