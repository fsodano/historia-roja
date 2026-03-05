import json
import requests
from datetime import datetime

all_matches = []

# List of leagues to check
leagues = [
    ("ARG.1", "Argentine Liga Profesional de Fútbol"),
    ("ARG.COPA_ARG", "Copa Argentina"),
    ("CONMEBOL.SUDAMERICANA", "Copa Sudamericana"),
    ("CONMEBOL.LIBERTADORES", "Copa Libertadores"),
]

for league_id, league_name in leagues:
    print(f"\n=== Checking {league_name} ({league_id}) ===")
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/teams/11/schedule"
    
    try:
        response = requests.get(url, params={"season": "2019"}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            events = data.get("events", [])
            print(f"Found {len(events)} events")
            
            for event in events:
                season_year = event.get("season", {}).get("year")
                if season_year == 2019:
                    match_date_str = event.get("date", "")
                    match_date = datetime.fromisoformat(match_date_str.replace('Z', '+00:00'))
                    print(f"  - {match_date.strftime('%d/%m/%Y')}: {event.get('name')}")
        else:
            print(f"HTTP {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# Try alternative endpoints
print("\n=== Checking team events endpoint ===")
url = "https://site.api.espn.com/apis/v2/sports/soccer/teams/11/events"
try:
    response = requests.get(url, params={"season": "2019"}, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found data")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Checking with different league formats ===")
leagues_alt = [
    "sud.3",
    "sud.1",
    "conmebol.sudamericana",
]
for league_id in leagues_alt:
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/teams/11/schedule"
    try:
        response = requests.get(url, params={"season": "2019"}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            events = data.get("events", [])
            print(f"{league_id}: {len(events)} events")
        else:
            print(f"{league_id}: HTTP {response.status_code}")
    except Exception as e:
        print(f"{league_id}: Error - {e}")
