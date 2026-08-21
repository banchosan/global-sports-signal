snapshot_70 = {
    "minute": 70,
    "home_shots": 12,
    "away_shots": 5,
    "home_shots_on_goal": 5,
    "away_shots_on_goal": 2,
    "home_corners": 7,
    "away_corners": 2,
    "home_xg": 1.42,
    "away_xg": 0.61
}

snapshot_80 = {
    "minute": 80,
    "home_shots": 17,
    "away_shots": 6,
    "home_shots_on_goal": 8,
    "away_shots_on_goal": 2,
    "home_corners": 10,
    "away_corners": 2,
    "home_xg": 2.03,
    "away_xg": 0.66
}

home_shots_diff = snapshot_80["home_shots"] - snapshot_70["home_shots"]
away_shots_diff = snapshot_80["away_shots"] - snapshot_70["away_shots"]

home_sog_diff = snapshot_80["home_shots_on_goal"] - snapshot_70["home_shots_on_goal"]
away_sog_diff = snapshot_80["away_shots_on_goal"] - snapshot_70["away_shots_on_goal"]

home_corners_diff = snapshot_80["home_corners"] - snapshot_70["home_corners"]
away_corners_diff = snapshot_80["away_corners"] - snapshot_70["away_corners"]

home_xg_diff = snapshot_80["home_xg"] - snapshot_70["home_xg"]
away_xg_diff = snapshot_80["away_xg"] - snapshot_70["away_xg"]

print("70分 → 80分の変化")
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