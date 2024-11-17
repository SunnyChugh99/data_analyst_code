import requests
from bs4 import BeautifulSoup

# URL of the tournament page
tournament_url = "https://www.espncricinfo.com/records/tournament/team-match-results/icc-men-s-t20-world-cup-2022-23-14450"

def get_match_results(tournament_url):
    response = requests.get(tournament_url)

    # Check if the response was successful
    if response.status_code == 200:
        # Parse the HTML content directly from the response
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table containing match results
        match_table = soup.find('table', class_=['ds-w-full', 'ds-table', 'ds-table-xs', 'ds-table-auto'])

        if match_table:
            results = []
            # Iterate through the rows of the table, skipping the header row
            for row in match_table.select('tbody > tr'):
                # Extracting match details (modify as per your requirement)
                cols = row.find_all('td')
                if cols:
                    match_info = {
                        "date": cols[0].text.strip(),
                        "team1": cols[1].text.strip(),
                        "team2": cols[2].text.strip(),
                        "result": cols[3].text.strip(),
                        "venue": cols[4].text.strip(),
                    }
                    results.append(match_info)

            return results
        else:
            print("Match table not found.")
            return None
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

# ------- MAIN FUNCTION --------- #
if __name__ == "__main__":
    match_results = get_match_results(tournament_url)
    if match_results:
        for match in match_results:
            print(match)
