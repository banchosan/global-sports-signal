import json

filename = "data/snapshots/snapshot_20260817_125158.json"

with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

print(data)

print("試合:", data["home_team"], "vs", data["away_team"])
print("時間:", data["minute"])
print("シュート:", data["home_shots"], "-", data["away_shots"])
print("xG:", data["home_xg"], "-", data["away_xg"])