import pandas as pd

from sign_recorder import SignRecorder


def _recorder(names):
    df = pd.DataFrame({"name": names, "sign_model": [None] * len(names), "distance": [1.0] * len(names)}, dtype=object)
    return SignRecorder(df)


def test_unanimous_batch_returns_the_sign():
    assert _recorder(["hello", "hello", "thanks"])._get_sign_predicted(batch_size=2, threshold=0.8) == "hello"


def test_split_batch_is_not_found():
    assert _recorder(["hello", "thanks"])._get_sign_predicted(batch_size=2, threshold=0.8) == "Sign Not Found"


def test_default_is_nearest_neighbour():
    # the code's defaults (batch_size=1, threshold=0.8) reduce voting to 1-NN, unlike the paper's batch_size=2
    assert _recorder(["thanks", "hello"])._get_sign_predicted() == "thanks"
