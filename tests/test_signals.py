from signals import (
    detect_corner_signal,
    detect_goal_signal,
    detect_comeback_signal,
)


# ==========================================
# CORNER SIGNAL TEST
# ==========================================
def test_home_corner_signal():

    # 60→70分でHOMEがかなり押している想定
    diff = {
        "minutes": 10,
        "home_shots": 5,
        "away_shots": 1,
        "home_sog": 2,
        "away_sog": 0,
        "home_corners": 3,
        "away_corners": 0,
        "home_xg": 0.6,
        "away_xg": 0.1,
    }

    home_score, away_score = detect_corner_signal(diff)

    # HOMEは強いシグナルになるはず
    assert home_score >= 2

    # AWAYは強いシグナルにならないはず
    assert away_score < 2


# ==========================================
# GOAL SIGNAL TEST
# ==========================================
def test_home_goal_signal():

    # 60→70でもHOMEが押している
    diff_60_70 = {
        "home_shots": 4,
        "away_shots": 1,
        "home_sog": 2,
        "away_sog": 0,
        "home_xg": 0.6,
        "away_xg": 0.1,
    }

    # 70→80でもHOMEが押し続けている
    diff_70_80 = {
        "home_shots": 5,
        "away_shots": 1,
        "home_sog": 3,
        "away_sog": 0,
        "home_xg": 0.61,
        "away_xg": 0.05,
    }

    home_score, away_score = detect_goal_signal(
        diff_60_70,
        diff_70_80
    )

    # HOMEは継続的に押しているので
    # Goal Signalが出るはず
    assert home_score >= 2

    # AWAYは出ないはず
    assert away_score < 2


# ==========================================
# COMEBACK SIGNAL TEST
# ==========================================
def test_home_comeback_signal():

    # 60分時点のスコア
    snapshot_60 = {
        "home_score": 0,
        "away_score": 1,
    }

    # 80分でもHOMEが0-1で負けている想定
    snapshot_80 = {
        "home_score": 0,
        "away_score": 1,
    }

    # HOMEが60→70で押している
    diff_60_70 = {
        "home_shots": 4,
        "away_shots": 1,
        "home_sog": 2,
        "away_sog": 0,
        "home_xg": 0.6,
        "away_xg": 0.1,
    }

    # HOMEが70→80でも押している
    diff_70_80 = {
        "home_shots": 5,
        "away_shots": 1,
        "home_sog": 3,
        "away_sog": 0,
        "home_xg": 0.61,
        "away_xg": 0.05,
    }

    home_score, away_score = detect_comeback_signal(
        snapshot_60,
        snapshot_80,
        diff_60_70,
        diff_70_80
    )

    # HOMEは負けていて、
    # なおかつ20分間押し続けているので
    # Comeback Signalが出るはず
    assert home_score >= 2

    # AWAYは出ないはず
    assert away_score < 2

    # ==========================================
# CORNER NO SIGNAL TEST
# ==========================================
def test_no_corner_signal():

    # 攻撃が弱い想定
    diff = {
        "minutes": 10,
        "home_shots": 1,
        "away_shots": 1,
        "home_sog": 0,
        "away_sog": 0,
        "home_corners": 0,
        "away_corners": 0,
        "home_xg": 0.08,
        "away_xg": 0.05,
    }

    home_score, away_score = detect_corner_signal(diff)

    # どちらにも強いCorner Signalは出ないはず
    assert home_score < 2
    assert away_score < 2


# ==========================================
# GOAL NO SIGNAL TEST
# ==========================================
def test_no_goal_signal():

    # 60→70も弱い
    diff_60_70 = {
        "home_shots": 1,
        "away_shots": 1,
        "home_sog": 0,
        "away_sog": 0,
        "home_xg": 0.08,
        "away_xg": 0.05,
    }

    # 70→80も弱い
    diff_70_80 = {
        "home_shots": 1,
        "away_shots": 1,
        "home_sog": 0,
        "away_sog": 0,
        "home_xg": 0.05,
        "away_xg": 0.04,
    }

    home_score, away_score = detect_goal_signal(
        diff_60_70,
        diff_70_80
    )

    # どちらにもGoal Signalは出ないはず
    assert home_score < 2
    assert away_score < 2


# ==========================================
# COMEBACK NO SIGNAL TEST
# ==========================================
def test_no_comeback_signal():

    # HOMEは負けている
    snapshot_60 = {
        "home_score": 0,
        "away_score": 1,
    }

    snapshot_80 = {
        "home_score": 0,
        "away_score": 1,
    }

    # でも攻撃は弱い
    diff_60_70 = {
        "home_shots": 1,
        "away_shots": 1,
        "home_sog": 0,
        "away_sog": 0,
        "home_xg": 0.08,
        "away_xg": 0.05,
    }

    diff_70_80 = {
        "home_shots": 1,
        "away_shots": 1,
        "home_sog": 0,
        "away_sog": 0,
        "home_xg": 0.05,
        "away_xg": 0.04,
    }

    home_score, away_score = detect_comeback_signal(
        snapshot_60,
        snapshot_80,
        diff_60_70,
        diff_70_80
    )

    # 負けていても押していないなら
    # Comeback Signalは出ないはず
    assert home_score < 2
    assert away_score < 2

    # ==========================================
# CORNER 境界値 TEST
# ==========================================
def test_corner_signal_boundary():

    # ------------------------------
    # Shots = 3
    # 最初の条件を満たさない
    # ------------------------------
    diff_shots_3 = {
        "minutes": 10,

        "home_shots": 3,
        "away_shots": 2,

        "home_sog": 1,
        "away_sog": 1,

        "home_corners": 2,
        "away_corners": 1,

        "home_xg": 0.2,
        "away_xg": 0.2,
    }

    # ------------------------------
    # Shotsだけ4に変更
    # 最初の条件を満たす
    # ------------------------------
    diff_shots_4 = {
        "minutes": 10,

        "home_shots": 4,
        "away_shots": 2,

        "home_sog": 1,
        "away_sog": 1,

        "home_corners": 2,
        "away_corners": 1,

        "home_xg": 0.2,
        "away_xg": 0.2,
    }

    score_3, _ = detect_corner_signal(diff_shots_3)
    score_4, _ = detect_corner_signal(diff_shots_4)

    # Shots 3ではこの条件による加点なし
    assert score_3 == 0

    # Shots 4になると条件成立して+1
    assert score_4 == 1