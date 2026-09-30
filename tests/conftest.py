"""Stub mediapipe and cv2 when they are not installed so the DTW and voting logic can be tested anywhere."""
import sys
import types


def _stub(name, **attrs):
    module = types.ModuleType(name)
    module.__dict__.update(attrs)
    sys.modules[name] = module


try:
    import mediapipe  # noqa: F401
except ImportError:
    holistic = types.SimpleNamespace(HAND_CONNECTIONS=frozenset({(0, 1), (1, 2)}))
    _stub("mediapipe", solutions=types.SimpleNamespace(holistic=holistic))

try:
    import cv2  # noqa: F401
except ImportError:
    _stub("cv2")
