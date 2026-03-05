import json
import requests
from datetime import datetime

# Read the JSON file that was already fetched
with open('/Users/fsodano/.local/share/opencode/tool-output/tool_cb4d65f4e001mNh5HII4XGoHz0', 'r') as f:
    data = json.load(f)

matches = []

for event in data.get("events", []):
    # Get the season year from the event
    season_year = event.get("season", {}).get("year")
    
    # For the 2019 season, ESPN includes matches played in early 2020
    # The "2019" season in Argentina runs from July 2019 to March 2020
    if season_year != 2019:
        continue
    
    # Get the actual match date
    match_date_str = event.get("date", "")
    match_date = datetime.fromisoformat(match_date_str.replace('Z', '+00:00'))
    
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
    ind_home_away = None
    
    for comp in competitors:
        team_name = comp.get("team", {}).get("displayName", "")
        score = comp.get("score", {}).get("value")
        is_home = comp.get("homeAway") == "home"
        is_winner = comp.get("winner", False)
        team_id = comp.get("team", {}).get("id", "")
        
        if is_home:
            home_team = team_name
            home_score = int(score) if score is not None else None
        else:
            away_team = team_name
            away_score = int(score) if score is not None else None
        
        # Check if this is Independiente (team ID 11)
        if team_id == "11":
            ind_winner = is_winner
            ind_home_away = "home" if is_home else "away"
    
    # Skip matches without scores
    if home_score is None or away_score is None:
        continue
    
    # Determine result from Independiente's perspective
    # A draw is when scores are equal
    if home_score == away_score:
        result = "DRAW"
    elif ind_winner:
        result = "WIN"
    else:
        result = "LOSS"
    
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
    print(f"Found match: {home_team} {home_score}-{away_score} {away_team} ({formatted_date}) - {result}")

# Sort matches by date
matches.sort(key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"))

print(f"\nTotal matches found: {len(matches)}")

# Save to JSON file
output_path = "/Users/fsodano/fibradev/historia-roja/data/2019_raw.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(matches, f, indent=2, ensure_ascii=False)

print(f"\nData saved to {output_path}")
