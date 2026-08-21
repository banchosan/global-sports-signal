import os
import requests
import json

from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("API_FOOTBALL_KEY")

fixture_id = 1556024

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": api_key
}

params = {
    "id": fixture_id
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

data = response.json()

print("HTTP Status:", response.status_code)
print("Errors:", data["errors"])
print("Results:", data["results"])

if data["results"] > 0:

    game = data["response"][0]

    print()
    print("=== MATCH ===")
    print(
        game["teams"]["home"]["name"],
        "vs",
        game["teams"]["away"]["name"]
    )

    print("Minute:", game["fixture"]["status"]["elapsed"])
    print("Score:", game["goals"]["home"], "-", game["goals"]["away"])

    print()
    print("=== STATISTICS BLOCK ===")

    statistics = game.get("statistics")

    print(json.dumps(
        statistics,
        ensure_ascii=False,
        indent=2
    ))