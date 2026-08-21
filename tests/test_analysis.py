# analysis.py にある差分計算関数を読み込む
from analysis import calculate_diff


# ==========================================
# 60分 → 70分の差分が
# 正しく計算されるかテスト
# ==========================================
def test_calculate_diff():

    # 60分時点
    snapshot_60 = {
        "minute": 60,
        "home_shots": 8,
        "away_shots": 5,
        "home_shots_on_goal": 3,
        "away_shots_on_goal": 2,
        "home_corners": 4,
        "away_corners": 2,
        "home_xg": 0.82,
        "away_xg": 0.45,
    }

    # 70分時点
    snapshot_70 = {
        "minute": 70,
        "home_shots": 12,
        "away_shots": 6,
        "home_shots_on_goal": 5,
        "away_shots_on_goal": 2,
        "home_corners": 7,
        "away_corners": 2,
        "home_xg": 1.42,
        "away_xg": 0.51,
    }

    # 差分計算
    diff = calculate_diff(snapshot_60, snapshot_70)

    # 正しい差分になっているか確認
    assert diff["minutes"] == 10

    assert diff["home_shots"] == 4
    assert diff["away_shots"] == 1

    assert diff["home_sog"] == 2
    assert diff["away_sog"] == 0

    assert diff["home_corners"] == 3
    assert diff["away_corners"] == 0

    assert round(diff["home_xg"], 2) == 0.60
    assert round(diff["away_xg"], 2) == 0.06