import requests
import pandas as pd
import time

api_url = "https://www.sofascore.com/api/v1/team/2829/events/last/0"
    
    # Set headers to mimic a browser
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.sofascore.com/fr/equipe/football/real-madrid/2829'
    }

response = requests.get(api_url, headers=headers)


if response.status_code == 200:
    data = response.json()
    events = data.get('events', [])
else:
    print(f"Failed to retrieve data: {response.status_code}")
    
results = []

for event in events:
    home_team = event['homeTeam']['name']
    away_team = event['awayTeam']['name']
    
    timestamp = event['startTimestamp']
    match_date = time.strftime('%Y-%m-%d', time.localtime(timestamp))
    
    competition = event['tournament']['name']
    
    if event['status']['type'] == 'finished':
        home_score = event['homeScore']['current']
        away_score = event['awayScore']['current']
        
        if home_team == "Real Madrid":
            goals_scored = event['homeScore']['current']
            goals_conceded = event['awayScore']['current']
            
        else:
            goals_scored = event['awayScore']['current']
            goals_conceded = event['homeScore']['current']
            
    results.append({
        'Home Team': home_team,
        'Away Team': away_team,
        'Match Date': match_date,
        'Competition': competition,
        'Goals Scored': goals_scored,
        'Goals Conceded': goals_conceded,
    })

df = pd.DataFrame(results)
if not df.empty:
    print(f"Successfully scraped {len(df)} matches")
    print(df)
        
    # Save to CSV
    df.to_csv("real_madrid_results.csv", index=False)
    print("Results saved to real_madrid_results.csv")