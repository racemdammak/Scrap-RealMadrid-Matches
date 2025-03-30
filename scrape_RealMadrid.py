import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_real_madrid_results():
    url = "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats"
    
    # Add headers to mimic a browser request
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    results_table = soup.find('table', {'id': 'matchlogs_for'})
    df = pd.read_html(str(results_table))[0]
    
    
    columns_to_drop = ['Time', 'Day', 'Captain', 'Attendance', 'Referee', 'Match Report', 'Notes']  # Replace 'Column1', 'Column2' with actual column names
    df.drop(columns=columns_to_drop, inplace=True)
    
    # Drop rows where the 'Result' column is NaN or empty
    df = df.dropna(subset=['Result'])
    df = df[df['Result'].str.strip() != '']
    
    return df

if __name__ == "__main__":
    print("Scraping Real Madrid Results...")
    results = scrape_real_madrid_results()
    
    if not results.empty:
        print(f"Successfully scraped {len(results)} matches")
        print(results)
        # Save to CSV
        results.to_csv("results.csv", index=False)
        print("Results saved to results.csv")
    else:
        print("Failed to scrape the data")