from pathlib import Path
from snapshot_storage import save_live_snapshot


def test_save_live_snapshot(tmp_path, monkeypatch):

    # テスト中だけ保存先を一時フォルダに変える
    monkeypatch.chdir(tmp_path)

    snapshot = {
        "fixture_id": 12345,
        "minute": 60,
        "home_team": "Team A",
        "away_team": "Team B",
        "home_score": 1,
        "away_score": 0,
        "home_shots": 10,
        "away_shots": 5,
        "home_shots_on_goal": 4,
        "away_shots_on_goal": 2,
        "home_corners": 6,
        "away_corners": 2,
        "home_xg": 1.2,
        "away_xg": 0.4,
    }

    save_live_snapshot(snapshot)

    expected_file = Path(
        "data/live_snapshots/12345_60.json"
    )

    assert expected_file.exists()