import requests
from bs4 import BeautifulSoup

# ------- STAGE 1: Collect Match Summary Links ------- #
def get_match_links(tournament_url):
    response = requests.get(tournament_url)
    
    # Check if the response was successful
    if response.status_code == 200:
        print("Response Content-Type:", response.headers.get('Content-Type'))
        print("Response Text:", response.text)  # Print the response for debugging
        
        # Attempt to parse JSON if Content-Type indicates JSON
        if 'application/json' in response.headers.get('Content-Type'):
            try:
                print("in if block")
                data = response.json()
                # Process your JSON data here
                print("Parsed JSON data:", data)
            except ValueError as e:
                print("Failed to parse JSON:", e)
        else:
            print("Response is not JSON. Handling as HTML.")
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all rows containing match links
            all_rows = soup.select('table.engineTable > tbody > tr.data1')
            links = []
            for row in all_rows:
                match_url = row.select_one('td:nth-of-type(7) a')['href']
                full_url = "https://www.espncricinfo.com" + match_url
                links.append(full_url)
            return links
                    # If it's HTML, you can continue with BeautifulSoup or another method
    else:
        print("Failed to retrieve data. Status code:", response.status_code)


# ------- STAGE 2: Extract Batting Summaries from Each Match ------- #

def get_batting_summary(match_url):
    # Fetch the match page
    response = requests.get(match_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract teams involved in the match
    match_info_div = soup.find('div', text="Match Details").find_parent()
    teams = match_info_div.find_all('span > span > span')
    team1, team2 = teams[0].text.replace(" Innings", ""), teams[1].text.replace(" Innings", "")
    match_info = f"{team1} Vs {team2}"

    # Extract batting data
    tables = soup.select('div > table.ci-scorecard-table')
    batting_summary = []

    for i, table in enumerate(tables[:2]):  # Only the first 2 tables (1st and 2nd innings)
        team_innings = team1 if i == 0 else team2
        rows = table.select('tbody > tr')
        
        # Loop through each row and extract relevant stats
        for index, row in enumerate(rows):
            tds = row.find_all('td')
            if len(tds) >= 8:
                batsman_name = tds[0].select_one('a > span > span').text.replace(' ', '')
                dismissal = tds[1].select_one('span > span').text
                runs = tds[2].select_one('strong').text
                balls = tds[3].text
                fours = tds[5].text
                sixes = tds[6].text
                sr = tds[7].text

                batting_summary.append({
                    "match": match_info,
                    "teamInnings": team_innings,
                    "battingPos": index + 1,
                    "batsmanName": batsman_name,
                    "dismissal": dismissal,
                    "runs": runs,
                    "balls": balls,
                    "4s": fours,
                    "6s": sixes,
                    "SR": sr
                })
    return batting_summary

# --------- MAIN FUNCTION --------- #

if __name__ == "__main__":
    tournament_url = "https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament"
    
    # Stage 1: Get match summary links
    match_links = get_match_links(tournament_url)
    print("match links")
    print(match_links)
    # Stage 2: Extract batting summaries for each match
    all_batting_summaries = []
    for match_url in match_links:
        match_summary = get_batting_summary(match_url)
        all_batting_summaries.extend(match_summary)
    
    # Print or process all batting summaries
    print(all_batting_summaries)

