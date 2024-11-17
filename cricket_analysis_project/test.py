import requests
from bs4 import BeautifulSoup

# -------------- STAGE 1 ------------
def stage_1():
    url = 'https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament'
    
    # Send GET request
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    })
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the table with the specified classes
    match_table = soup.find('table', class_=['ds-w-full', 'ds-table', 'ds-table-xs', 'ds-table-auto'])
    
    # Ensure the table was found
    if not match_table:
        print("Match table not found.")
        return []
    
    # Extract match summary links
    links = []
    for row in match_table.select('tbody > tr'):
        row_url = "https://www.espncricinfo.com" + row.find_all('td')[6].find('a')['href']
        links.append(row_url)

    return links


# -------------- STAGE 2 ------------
def stage_2(match_url):
    print("match url-1")
    print(match_url)

    print("match url-2")
    # Send GET request to match page
    response = requests.get(match_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    print("soup donedone")

    soup = BeautifulSoup(response.text, 'html.parser')
        # Find the table containing match results
    tables = soup.find('table', class_="ci-scorecard-table")


    print("table")
    print(tables)
    player_data = []

    player_data = []  # List to store player data for both innings

    for table_index, table in enumerate(tables):
        rows = table.select('tbody > tr')
        
        for row in rows:
            # Skip hidden rows
            if 'ds-hidden' in row.get('class', []):
                continue
            
            # Extract player details
            player_name = row.select_one('td a').get_text(strip=True) if row.select_one('td a') else ''
            dismissal = row.select_one('td:nth-of-type(2)').get_text(strip=True) if row.select_one('td:nth-of-type(2)') else ''
            runs = row.select_one('td:nth-of-type(3)').get_text(strip=True) if row.select_one('td:nth-of-type(3)') else ''
            balls = row.select_one('td:nth-of-type(4)').get_text(strip=True) if row.select_one('td:nth-of-type(4)') else ''
            fours = row.select_one('td:nth-of-type(6)').get_text(strip=True) if row.select_one('td:nth-of-type(6)') else ''
            sixes = row.select_one('td:nth-of-type(7)').get_text(strip=True) if row.select_one('td:nth-of-type(7)') else ''
            strike_rate = row.select_one('td:nth-of-type(8)').get_text(strip=True) if row.select_one('td:nth-of-type(8)') else ''
            
            # Append the data to the list with team information based on the inning
            player_data.append({
                'Inning': table_index + 1,  # Inning number (1 for first inning, 2 for second)
                'Player': player_name,
                'Dismissal': dismissal,
                'Runs': runs,
                'Balls': balls,
                '4s': fours,
                '6s': sixes,
                'SR': strike_rate
            })

    # Example of how to use player_data
    for entry in player_data:
        print(entry)



# Main function to execute both stages
if __name__ == "__main__":
    # Stage 1: Get match summary links
    match_links = stage_1()
    print("match links")
    print(match_links)
    # Stage 2: Collect data for each match link
    all_batting_summaries = []
    # for link in match_links:
    #     summary = stage_2(link)
    #     break
    #     all_batting_summaries.append(summary)
    link = match_links[0]
    summary = stage_2(link)

    print("batting")
    print(all_batting_summaries)
    # Print or process all summaries
    for batting_summary in all_batting_summaries:
        print(batting_summary)
