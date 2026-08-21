import os
import requests
from dotenv import load_dotenv

from snapshot_builder import build_snapshot
from snapshot_storage import save_live_snapshot
from live_snapshot_analyzer import analyze_latest_snapshots


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

    print(
        league_name,
        "-",
        country,
        "-",
        game["teams"]["home"]["name"],
        "vs",
        game["teams"]["away"]["name"]
    )

    # ==========================================
    # 対象リーグ
    # ==========================================
    if (
        (league_name == "Major League Soccer" and country == "USA")
        or
        (league_name == "J1 League" and country == "Japan")
    ):

        fixture_id = game["fixture"]["id"]

        print()
        print(
            "対象試合:",
            game["teams"]["home"]["name"],
            "vs",
            game["teams"]["away"]["name"]
        )

        print("Fixture ID:", fixture_id)

        # ==========================================
        # 試合statistics取得
        # ==========================================
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

        # ==========================================
        # statisticsが取れた場合のみ処理
        # ==========================================
        if stats_data["results"] > 0:

            home_data = stats_data["response"][0]
            away_data = stats_data["response"][1]

            home_stats = {}
            away_stats = {}

            for stat in home_data["statistics"]:
                home_stats[stat["type"]] = stat["value"]

            for stat in away_data["statistics"]:
                away_stats[stat["type"]] = stat["value"]

            # ==========================================
            # HOME statistics表示
            # ==========================================
            print()
            print(home_data["team"]["name"])
            print("Shots:", home_stats.get("Total Shots"))
            print("SOT:", home_stats.get("Shots on Goal"))
            print("Corners:", home_stats.get("Corner Kicks"))
            print("Possession:", home_stats.get("Ball Possession"))
            print("xG:", home_stats.get("expected_goals"))

            # ==========================================
            # AWAY statistics表示
            # ==========================================
            print()
            print(away_data["team"]["name"])
            print("Shots:", away_stats.get("Total Shots"))
            print("SOT:", away_stats.get("Shots on Goal"))
            print("Corners:", away_stats.get("Corner Kicks"))
            print("Possession:", away_stats.get("Ball Possession"))
            print("xG:", away_stats.get("expected_goals"))

            # ==========================================
            # 実際のAPIデータからsnapshotを作る
            # ==========================================
            minute = game["fixture"]["status"]["elapsed"]

            home_score = game["goals"]["home"]
            away_score = game["goals"]["away"]

            snapshot = build_snapshot(
                fixture_id=fixture_id,
                minute=minute,
                home_team=game["teams"]["home"]["name"],
                away_team=game["teams"]["away"]["name"],
                home_score=home_score,
                away_score=away_score,
                statistics_response=stats_data,
            )

            print()
            print("=== SNAPSHOT ===")
            print(snapshot)

            # ==========================================
            # snapshot保存
            # ==========================================
            save_live_snapshot(snapshot)
            analyze_latest_snapshots(fixture_id)