import os
import json
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("API_FOOTBALL_KEY")

headers = {
    "x-apisports-key": api_key
}

# -------------------------
# 1. 前回のsnapshotを読み込む
# -------------------------

previous_snapshot = None

if os.path.exists("snapshot.json"):
    with open("snapshot.json", "r") as file:
        previous_snapshot = json.load(file)

    print("前回の状態:")
    print(previous_snapshot)


# -------------------------
# 2. 現在のライブ試合を取得
# -------------------------

fixtures_url = "https://v3.football.api-sports.io/fixtures"

fixtures_params = {
    "live": "all"
}

response = requests.get(
    fixtures_url,
    headers=headers,
    params=fixtures_params
)

data = response.json()


# -------------------------
# 3. 前回と同じ試合を探す
# -------------------------

for game in data["response"]:

    fixture_id = game["fixture"]["id"]

    if (
        previous_snapshot is not None
        and fixture_id == previous_snapshot["fixture_id"]
    ):

        home_name = game["teams"]["home"]["name"]
        away_name = game["teams"]["away"]["name"]
        minute = game["fixture"]["status"]["elapsed"]

        # -------------------------
        # 4. 現在のstatisticsを取得
        # -------------------------

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

        if stats_data["results"] > 0:

            home_data = stats_data["response"][0]

            home_stats = {}

            for stat in home_data["statistics"]:
                home_stats[stat["type"]] = stat["value"]

            current_snapshot = {
                "fixture_id": fixture_id,
                "minute": minute,
                "team": home_name,
                "opponent": away_name,
                "shots": home_stats["Total Shots"],
                "sot": home_stats["Shots on Goal"],
                "corners": home_stats["Corner Kicks"],
                "xg": home_stats["expected_goals"]
            }

            print()
            print("現在の状態:")
            print(current_snapshot)


            # -------------------------
            # 5. 前回との差分を計算
            # -------------------------

            shots_change = (
                current_snapshot["shots"]
                - previous_snapshot["shots"]
            )

            sot_change = (
                current_snapshot["sot"]
                - previous_snapshot["sot"]
            )

            corners_change = (
                current_snapshot["corners"]
                - previous_snapshot["corners"]
            )

            xg_change = round(
                float(current_snapshot["xg"])
                - float(previous_snapshot["xg"]),
                2
            )


            # -------------------------
            # 6. 差分を表示
            # -------------------------

            print()
            print(
                previous_snapshot["minute"],
                "分 →",
                current_snapshot["minute"],
                "分"
            )

            print("Shots:", shots_change)
            print("SOT:", sot_change)
            print("Corners:", corners_change)
            print("xG:", xg_change)


            # -------------------------
            # 7. 現在の状態でsnapshotを更新
            # -------------------------

            with open("snapshot.json", "w") as file:
                json.dump(current_snapshot, file, indent=2)

            print()
            print("snapshotを更新しました")

        break