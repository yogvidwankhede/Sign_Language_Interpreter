import numpy as np
import pandas as pd

from models.sign_model import SignModel
from utils.dtw import dtw_distances


def _hand(seed, frames=10):
    return np.random.default_rng(seed).random((frames, 63)) + 1


def _refs(models):
    data = {"name": [n for n, _ in models], "sign_model": [m for _, m in models], "distance": [0] * len(models)}
    return pd.DataFrame(data, dtype=object)


def test_identical_sign_ranks_first_with_zero_distance():
    right_only = lambda seed: SignModel(np.zeros((10, 63)), _hand(seed))
    refs = _refs([("B", right_only(2)), ("A", right_only(1)), ("C", right_only(3))])
    ranked = dtw_distances(right_only(1), refs)
    assert list(ranked["name"])[0] == "A"
    assert float(ranked["distance"].iloc[0]) == 0.0
    assert all(float(d) > 0 for d in ranked["distance"].iloc[1:])


def test_distances_are_written_back():
    refs = _refs([("A", SignModel(_hand(1), np.zeros((10, 63)))), ("B", SignModel(_hand(2), np.zeros((10, 63))))])
    ranked = dtw_distances(SignModel(_hand(1), np.zeros((10, 63))), refs)
    assert float(ranked.set_index("name").loc["B", "distance"]) > 0


def test_reference_with_different_hands_is_infinite():
    left = SignModel(_hand(1), np.zeros((10, 63)))
    right = SignModel(np.zeros((10, 63)), _hand(1))
    ranked = dtw_distances(left, _refs([("L", left), ("R", right)]))
    assert list(ranked["name"]) == ["L", "R"]
    assert np.isinf(float(ranked["distance"].iloc[1]))
