"""Reproduce the accuracy table in the README.

Runs 5-fold cross-validation over all matches and a chronological test
(train on 2008–2021, test on 2022–2024) for each of the six models.

    python evaluate.py
"""

from __future__ import annotations

import warnings

import numpy as np
from sklearn.model_selection import StratifiedKFold

import app

warnings.filterwarnings("ignore")


def accuracy(train, test) -> dict[str, float]:
    app.MODELS = app.build_models(train)
    actual = (test["Winner_of_Match"] == test["Team_1"]).astype(int).to_numpy()
    return {key: float((app.team1_wins(key, test[app.FEATURES]) == actual).mean()) for key in app.ALGORITHMS}


def main() -> None:
    data = app.TRAINING_DATA
    target = (data["Winner_of_Match"] == data["Team_1"]).astype(int)

    folds: dict[str, list[float]] = {key: [] for key in app.ALGORITHMS}
    for train_idx, test_idx in StratifiedKFold(5, shuffle=True, random_state=42).split(data, target):
        for key, value in accuracy(data.iloc[train_idx], data.iloc[test_idx]).items():
            folds[key].append(value)

    season = app.RAW_MATCHES.loc[data.index, "season"].astype(str).str[:4].astype(int)
    future = accuracy(data[season <= 2021], data[season > 2021])
    toss = float((data["Toss_Winner"] == data["Winner_of_Match"]).mean())

    print(f"{'Model':28s} {'5-fold CV':>14s} {'2022–24 test':>13s}")
    for key in sorted(folds, key=lambda k: -np.mean(folds[k])):
        print(f"{app.ALGORITHMS[key]:28s} {np.mean(folds[key]):8.1%} ± {np.std(folds[key]):4.1%} {future[key]:12.1%}")
    print(f"{'Baseline: toss winner wins':28s} {toss:8.1%}")


if __name__ == "__main__":
    main()
