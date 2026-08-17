import os
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("API_FOOTBALL_KEY")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": api_key
}

params = {
    "live": "all"
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

data = response.json()

print("Status:", response.status_code)
print("試合数:", data["results"])


for game in data["response"]:
    league_name = game["league"]["name"]
    country = game["league"]["country"]

    if league_name == "2. Bundesliga" and country == "Germany":
        fixture_id = game["fixture"]["id"]

        print(
            "対象試合:",
            game["teams"]["home"]["name"],
            "vs",
            game["teams"]["away"]["name"]
        )

        print("Fixture ID:", fixture_id)

        stats_url = "https://v3.football.api-sports.io/fixtures/statistics"

        stats_params = {
            "fixture": fixture_id
        }

        stats_response = requests.get(
            stats_url,
            headers=headers,
            params=stats_params
        )

        stats_data = stats_response.json()

        print("Stats HTTP Status:", stats_response.status_code)
        print("Errors:", stats_data["errors"])
        print("Results:", stats_data["results"])

        if stats_data["results"] > 0:
            home_data = stats_data["response"][0]
            away_data = stats_data["response"][1]

            home_stats = {}
            away_stats = {}

            for stat in home_data["statistics"]:
                home_stats[stat["type"]] = stat["value"]

            for stat in away_data["statistics"]:
                away_stats[stat["type"]] = stat["value"]

            print()
            print(home_data["team"]["name"])
            print("Shots:", home_stats["Total Shots"])
            print("SOT:", home_stats["Shots on Goal"])
            print("Corners:", home_stats["Corner Kicks"])
            print("Possession:", home_stats["Ball Possession"])
            print("xG:", home_stats["expected_goals"])

            print()
            print(away_data["team"]["name"])
            print("Shots:", away_stats["Total Shots"])
            print("SOT:", away_stats["Shots on Goal"])
            print("Corners:", away_stats["Corner Kicks"])
            print("Possession:", away_stats["Ball Possession"])
            print("xG:", away_stats["expected_goals"])