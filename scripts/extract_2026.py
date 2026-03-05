#!/usr/bin/env python3
"""
Extract match data from ESPN for Club Atlético Independiente (2019-2026)
Save as CSV files in data/ directory
"""

import json
import sys

# Matches data extracted from ESPN
matches_2026 = [
    {"date":"Sáb., 28 de Feb.","competition":"Liga Profesional de Fútbol","home_team":"Independiente","away_team":"Central Córdoba (Santiago del Estero)","home_score":2,"away_score":0,"result":"WIN"},
    {"date":"Mar., 24 de Feb.","competition":"Liga Profesional de Fútbol","home_team":"Gimnasia (Mendoza)","away_team":"Independiente","home_score":1,"away_score":1,"result":"DRAW"},
    {"date":"Sáb., 21 de Feb.","competition":"Liga Profesional de Fútbol","home_team":"Independiente Rivadavia","away_team":"Independiente","home_score":3,"away_score":2,"result":"LOSS"},
    {"date":"Vie., 13 de Feb.","competition":"Liga Profesional de Fútbol","home_team":"Independiente","away_team":"Lanús","home_score":2,"away_score":0,"result":"WIN"},
    {"date":"Dom., 8 de Feb.","competition":"Liga Profesional de Fútbol","home_team":"Platense","away_team":"Independiente","home_score":0,"away_score":1,"result":"WIN"},
    {"date":"Sáb., 31 de Ene.","competition":"Liga Profesional de Fútbol","home_team":"Independiente","away_team":"Vélez Sarsfield","home_score":1,"away_score":1,"result":"DRAW"},
    {"date":"Mar., 27 de Ene.","competition":"Liga Profesional de Fútbol","home_team":"Newell's Old Boys","away_team":"Independiente","home_score":1,"away_score":1,"result":"DRAW"},
    {"date":"Vie., 23 de Ene.","competition":"Liga Profesional de Fútbol","home_team":"Independiente","away_team":"Estudiantes de La Plata","home_score":1,"away_score":1,"result":"DRAW"}
]

# Save raw JSON
with open('data/2026_raw.json', 'w', encoding='utf-8') as f:
    json.dump(matches_2026, f, indent=2, ensure_ascii=False)

print(f"Saved {len(matches_2026)} matches for 2026")
