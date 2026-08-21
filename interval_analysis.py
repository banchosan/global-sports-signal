import json
from pathlib import Path

from analysis import calculate_diff

from signals import (
    detect_corner_signal,
    detect_goal_signal,
    detect_comeback_signal,
)


# ==========================================
# JSON snapshotを読み込む
# ==========================================
def load_snapshot(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================
# 差分スタッツを見やすく表示
# ==========================================
def print_interval(title, diff):
    print()
    print(f"=== {title} ===")
    print("Minutes:", diff["minutes"])
    print("Shots:", diff["home_shots"], "-", diff["away_shots"])
    print("Shots on Goal:", diff["home_sog"], "-", diff["away_sog"])
    print("Corners:", diff["home_corners"], "-", diff["away_corners"])
    print(
        "xG:",
        round(diff["home_xg"], 2),
        "-",
        round(diff["away_xg"], 2)
    )


# ==========================================
# live snapshot一覧を取得
# ==========================================
folder = Path("data/live_snapshots")

files = list(folder.glob("*.json"))

if not files:
    print("ライブsnapshotがまだありません。")
    raise SystemExit


# ==========================================
# fixture_idごとにまとめる
# ==========================================
matches = {}

for file in files:
    snapshot = load_snapshot(file)

    fixture_id = snapshot["fixture_id"]

    if fixture_id not in matches:
        matches[fixture_id] = []

    matches[fixture_id].append(snapshot)


# ==========================================
# 各試合をminute順に並べて分析
# ==========================================
for fixture_id, snapshots in matches.items():

    snapshots.sort(key=lambda snapshot: snapshot["minute"])

    print()
    print("=" * 50)
    print("Fixture ID:", fixture_id)
    print(
        snapshots[0]["home_team"],
        "vs",
        snapshots[0]["away_team"]
    )

    # snapshotが1個しかない
    if len(snapshots) < 2:
        print("snapshotが1件だけなので、まだ差分分析できません。")
        continue

    # 最新2件
    old = snapshots[-2]
    new = snapshots[-1]

    diff_latest = calculate_diff(old, new)

    title = f'{old["minute"]} → {new["minute"]}'

    print_interval(title, diff_latest)

    # ======================================
    # CORNER SIGNAL
    # 最新区間だけでも判定できる
    # ======================================
    home_corner_score, away_corner_score = detect_corner_signal(
        diff_latest
    )

    print()
    print("=== CORNER SIGNAL ===")
    print("Home Corner Score:", home_corner_score)
    print("Away Corner Score:", away_corner_score)

    if home_corner_score >= 2:
        print("🚩 HOME CORNER SIGNAL")

    if away_corner_score >= 2:
        print("🚩 AWAY CORNER SIGNAL")

    # ======================================
    # snapshotが3件以上なら
    # 2区間を使うGoal / Comebackも判定
    # ======================================
    if len(snapshots) >= 3:

        first = snapshots[-3]
        middle = snapshots[-2]
        last = snapshots[-1]

        diff_first = calculate_diff(first, middle)
        diff_second = calculate_diff(middle, last)

        home_goal_score, away_goal_score = detect_goal_signal(
            diff_first,
            diff_second
        )

        print()
        print("=== GOAL SIGNAL ===")
        print("Home Goal Score:", home_goal_score)
        print("Away Goal Score:", away_goal_score)

        if home_goal_score >= 2:
            print("🔥 HOME GOAL SIGNAL")

        if away_goal_score >= 2:
            print("🔥 AWAY GOAL SIGNAL")

        home_comeback_score, away_comeback_score = detect_comeback_signal(
            first,
            last,
            diff_first,
            diff_second
        )

        print()
        print("=== COMEBACK SIGNAL ===")
        print("Home Comeback Score:", home_comeback_score)
        print("Away Comeback Score:", away_comeback_score)

        if home_comeback_score >= 2:
            print("⚡ HOME COMEBACK SIGNAL")

        if away_comeback_score >= 2:
            print("⚡ AWAY COMEBACK SIGNAL")

    else:
        print()
        print("snapshotが2件なので、Goal / Comeback判定にはもう1件必要です。")