import json
import requests
from datetime import datetime

# ESPN API endpoint for team schedule
url = "https://site.api.espn.com/apis/site/v2/sports/soccer/ARG.1/teams/11/schedule"

# Fetch data
response = requests.get(url, params={"season": "2019"})
data = response.json()

matches = []

for event in data.get("events", []):
    # Get the season year from the event
    season_year = event.get("season", {}).get("year")
    
    # Get the actual match date
    match_date_str = event.get("date", "")
    match_date = datetime.fromisoformat(match_date_str.replace('Z', '+00:00'))
    match_year = match_date.year
    
    # Only include matches from 2019
    if match_year != 2019:
        continue
    
    # Extract competition info
    competition = event.get("league", {}).get("name", "Unknown")
    season_type = event.get("seasonType", {}).get("name", "")
    
    # Get competitors
    competitors = event.get("competitions", [{}])[0].get("competitors", [])
    
    if len(competitors) != 2:
        continue
    
    home_team = None
    away_team = None
    home_score = None
    away_score = None
    ind_winner = None
    
    for comp in competitors:
        team_name = comp.get("team", {}).get("displayName", "")
        score = comp.get("score", {}).get("value", 0)
        is_home = comp.get("homeAway") == "home"
        is_winner = comp.get("winner", False)
        team_id = comp.get("team", {}).get("id", "")
        
        if is_home:
            home_team = team_name
            home_score = int(score) if score is not None else 0
        else:
            away_team = team_name
            away_score = int(score) if score is not None else 0
        
        # Check if this is Independiente (team ID 11)
        if team_id == "11":
            ind_winner = is_winner
    
    # Determine result from Independiente's perspective
    if ind_winner is True:
        result = "WIN"
    elif ind_winner is False:
        result = "LOSS"
    else:
        result = "DRAW"
    
    # Format date as DD/MM/YYYY
    formatted_date = match_date.strftime("%d/%m/%Y")
    
    match_data = {
        "date": formatted_date,
        "competition": competition,
        "home_team": home_team,
        "away_team": away_team,
        "home_score": home_score,
        "away_score": away_score,
        "result": result
    }
    
    matches.append(match_data)
    print(f"Found match: {home_team} {home_score}-{away_score} {away_team} ({formatted_date})")

# Sort matches by date
matches.sort(key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"))

print(f"\nTotal matches found: {len(matches)}")

# Save to JSON file
output_path = "/Users/fsodano/fibradev/historia-roja/data/2019_raw.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(matches, f, indent=2, ensure_ascii=False)

print(f"Data saved to {output_path}")
