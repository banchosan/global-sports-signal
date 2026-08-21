import json
from datetime import datetime
from pathlib import Path

sample_data = {
    "fixture_id": 123456,
    "minute": 70,
    "home_team": "Team A",
    "away_team": "Team B",
    "home_score": 1,
    "away_score": 1,
    "home_shots": 12,
    "away_shots": 5,
    "home_shots_on_goal": 5,
    "away_shots_on_goal": 2,
    "home_corners": 7,
    "away_corners": 2,
    "home_xg": 1.42,
    "away_xg": 0.61
}

folder = Path("data/snapshots")
folder.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

filename = folder / f"snapshot_{timestamp}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(sample_data, f, ensure_ascii=False, indent=2)

print(f"保存しました: {filename}")