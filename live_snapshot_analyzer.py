import json
from pathlib import Path

from analysis import calculate_diff
from signals import detect_corner_signal


def load_snapshot(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_latest_snapshots(fixture_id):
    folder = Path("data/live_snapshots")

    files = list(folder.glob(f"{fixture_id}_*.json"))

    if len(files) < 2:
        print("分析にはsnapshotが2件以上必要です。")
        return

    snapshots = []

    for file in files:
        snapshot = load_snapshot(file)
        snapshots.append(snapshot)

    snapshots.sort(
        key=lambda snapshot: snapshot["minute"]
    )

    old = snapshots[-2]
    new = snapshots[-1]

    diff = calculate_diff(old, new)

    print()
    print(
        f'=== {old["minute"]} → {new["minute"]} ==='
    )

    print(
        "Shots:",
        diff["home_shots"],
        "-",
        diff["away_shots"]
    )

    print(
        "Shots on Goal:",
        diff["home_sog"],
        "-",
        diff["away_sog"]
    )

    print(
        "Corners:",
        diff["home_corners"],
        "-",
        diff["away_corners"]
    )

    print(
        "xG:",
        round(diff["home_xg"], 2),
        "-",
        round(diff["away_xg"], 2)
    )

    home_score, away_score = detect_corner_signal(diff)

    print()
    print("=== CORNER SIGNAL ===")
    print("Home Corner Score:", home_score)
    print("Away Corner Score:", away_score)

    if home_score >= 2:
        print("🚩 HOME CORNER SIGNAL")

    if away_score >= 2:
        print("🚩 AWAY CORNER SIGNAL")