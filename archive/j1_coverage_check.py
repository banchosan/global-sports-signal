import os
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("API_FOOTBALL_KEY")

url = "https://v3.football.api-sports.io/leagues"

headers = {
    "x-apisports-key": api_key
}

params = {
    "name": "J1 League",
    "country": "Japan"
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


for league in data["response"]:

    print()
    print("League:", league["league"]["name"])
    print("Country:", league["country"]["name"])

    for season in league["seasons"]:

        if season["year"] == 2026:

            coverage = season["coverage"]

            print()
            print("=== 2026 COVERAGE ===")
            print("Fixtures:", coverage["fixtures"])