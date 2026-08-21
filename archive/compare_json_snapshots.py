import json


def load_snapshot(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


old = load_snapshot("data/snapshots/team_a_70.json")
new = load_snapshot("data/snapshots/team_a_80.json")


home_shots_diff = new["home_shots"] - old["home_shots"]
away_shots_diff = new["away_shots"] - old["away_shots"]

home_sog_diff = new["home_shots_on_goal"] - old["home_shots_on_goal"]
away_sog_diff = new["away_shots_on_goal"] - old["away_shots_on_goal"]

home_corners_diff = new["home_corners"] - old["home_corners"]
away_corners_diff = new["away_corners"] - old["away_corners"]

home_xg_diff = new["home_xg"] - old["home_xg"]
away_xg_diff = new["away_xg"] - old["away_xg"]


print(
    f'{old["minute"]}分 → {new["minute"]}分 '
    f'{old["home_team"]} vs {old["away_team"]}'
)

print("Home Shots:", home_shots_diff)
print("Away Shots:", away_shots_diff)
print("Home Shots on Goal:", home_sog_diff)
print("Away Shots on Goal:", away_sog_diff)
print("Home Corners:", home_corners_diff)
print("Away Corners:", away_corners_diff)
print("Home xG:", round(home_xg_diff, 2))
print("Away xG:", round(away_xg_diff, 2))


if home_shots_diff >= 4 and home_sog_diff >= 2 and home_xg_diff >= 0.4:
    print("🔥 HOME PRESSURE SIGNAL")

if away_shots_diff >= 4 and away_sog_diff >= 2 and away_xg_diff >= 0.4:
    print("🔥 AWAY PRESSURE SIGNAL")