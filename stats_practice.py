stats_60 = {
    "Total Shots": 8,
    "Shots on Goal": 2,
    "Corner Kicks": 3,
    "expected_goals": 1.33
}

stats_70 = {
    "Total Shots": 14,
    "Shots on Goal": 5,
    "Corner Kicks": 7,
    "expected_goals": 2.01
}


shots_change = stats_70["Total Shots"] - stats_60["Total Shots"]

print("直近10分のシュート:", shots_change)

sot_change = stats_70["Shots on Goal"] - stats_60["Shots on Goal"]

corners_change = stats_70["Corner Kicks"] - stats_60["Corner Kicks"]

xg_change = stats_70["expected_goals"] - stats_60["expected_goals"]


print("直近10分のシュート:", shots_change)
print("直近10分の枠内シュート:", sot_change)
print("直近10分のコーナー:", corners_change)
print("直近10分のxG:", xg_change)