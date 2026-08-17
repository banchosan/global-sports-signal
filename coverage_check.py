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
    "name": "Eredivisie"
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

data = response.json()

print("Status:", response.status_code)
print("Results:", data["results"])
print(data["response"])