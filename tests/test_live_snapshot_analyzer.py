import json
from pathlib import Path

from live_snapshot_analyzer import analyze_latest_snapshots


def test_analyze_latest_snapshots(tmp_path, monkeypatch, capsys):

    # テスト中だけ作業場所を一時フォルダに変更
    monkeypatch.chdir(tmp_path)

    folder = Path("data/live_snapshots")
    folder.mkdir(parents=True, exist_ok=True)

    snapshot_60 = {
        "fixture_id": 99999,
        "minute": 60,
        "home_team": "Team A",
        "away_team": "Team B",
        "home_score": 0,
        "away_score": 0,
        "home_shots": 5,
        "away_shots": 4,
        "home_shots_on_goal": 1,
        "away_shots_on_goal": 1,
        "home_corners": 2,
        "away_corners": 2,
        "home_xg": 0.30,
        "away_xg": 0.25,
    }

    snapshot_70 = {
        "fixture_id": 99999,
        "minute": 70,
        "home_team": "Team A",
        "away_team": "Team B",
        "home_score": 0,
        "away_score": 0,
        "home_shots": 10,
        "away_shots": 5,
        "home_shots_on_goal": 3,
        "away_shots_on_goal": 1,
        "home_corners": 5,
        "away_corners": 2,
        "home_xg": 0.95,
        "away_xg": 0.30,
    }

    with open(folder / "99999_60.json", "w", encoding="utf-8") as f:
        json.dump(snapshot_60, f)

    with open(folder / "99999_70.json", "w", encoding="utf-8") as f:
        json.dump(snapshot_70, f)

    analyze_latest_snapshots(99999)

    output = capsys.readouterr().out

    assert "60 → 70" in output
    assert "Shots: 5 - 1" in output
    assert "Corners: 3 - 0" in output
    assert "HOME CORNER SIGNAL" in output