#!/usr/bin/env python3
"""
Scraper for Independiente matches from josecarluccio.blogspot.com
Extracts all matches for a given year and saves to CSV
"""

import requests
import re
import csv
import sys
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_year(year):
    """Fetch all posts for a given year from the blog"""
    url = f"https://josecarluccio.blogspot.com/search/label/{year}?max-results=100&start=0&by-date=false"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {year}: {e}")
        return None

def parse_matches(html_content, year):
    """Parse Independiente matches from HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all post content
    posts = soup.find_all('div', class_='post-body')
    
    matches = []
    
    for post in posts:
        text = post.get_text()
        
        # Look for match patterns
        # Pattern: "DD/MM/YYYY en Location: Team1 X, Team2 Y"
        match_pattern = r'(\d{2}/\d{2}/\d{4})\s+en\s+([^:]+):\s+([^\d]+)\s+(\d+)\s*,\s*([^\d]+)\s+(\d+)'
        
        for match in re.finditer(match_pattern, text):
            date_str = match.group(1)
            location = match.group(2).strip()
            team1 = match.group(3).strip()
            score1 = int(match.group(4))
            team2 = match.group(5).strip()
            score2 = int(match.group(6))
            
            # Check if Independiente is playing
            team1_lower = team1.lower()
            team2_lower = team2.lower()
            
            if 'independiente' in team1_lower or 'independiente' in team2_lower:
                # Determine home/away and result from Independiente's perspective
                if 'independiente' in team1_lower:
                    home_team = team1
                    away_team = team2
                    home_score = score1
                    away_score = score2
                    ind_score = score1
                    opp_score = score2
                else:
                    home_team = team1
                    away_team = team2
                    home_score = score1
                    away_score = score2
                    ind_score = score2
                    opp_score = score1
                
                # Determine result
                if ind_score > opp_score:
                    result = 'WIN'
                elif ind_score < opp_score:
                    result = 'LOSS'
                else:
                    result = 'DRAW'
                
                # Try to determine competition
                competition = 'Primera División'  # default
                if 'copa' in text.lower()[:text.find(date_str)].lower():
                    # Look for competition name before the match
                    comp_match = re.search(r'Copa\s+["\']?([^"\']+)["\']?', text[:text.find(date_str)])
                    if comp_match:
                        competition = f"Copa {comp_match.group(1)}"
                
                matches.append({
                    'date': date_str,
                    'competition': competition,
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_score': home_score,
                    'away_score': away_score,
                    'result': result
                })
    
    return matches

def save_to_csv(matches, year):
    """Save matches to CSV file"""
    if not matches:
        print(f"No matches found for {year}")
        return
    
    filename = f"data/{year}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'competition', 'home_team', 'away_team', 'home_score', 'away_score', 'result'])
        writer.writeheader()
        writer.writerows(matches)
    
    print(f"Saved {len(matches)} matches to {filename}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python scrape_year.py <year>")
        sys.exit(1)
    
    year = sys.argv[1]
    
    print(f"Fetching data for {year}...")
    html = fetch_year(year)
    
    if html:
        print(f"Parsing matches for {year}...")
        matches = parse_matches(html, year)
        save_to_csv(matches, year)
    else:
        print(f"Failed to fetch data for {year}")

if __name__ == "__main__":
    main()
