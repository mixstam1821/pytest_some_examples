"""
Core pytest patterns: plain asserts, exception testing, float comparisons,
and grouping related tests in a class.
"""
import numpy as np
import pytest

from src.pipeline import adaptive_qa_threshold, kelvin_to_celsius


def test_adaptive_threshold_returns_loosest_that_passes():
    qa = np.array([0.8, 0.8, 0.2, 0.2])  # 50% >= 0.75, 100% >= 0.25... etc
    result = adaptive_qa_threshold(qa, min_valid_fraction=0.5)
    assert result == 0.75


def test_adaptive_threshold_falls_back_to_zero_when_nothing_passes():
    qa = np.array([0.1, 0.05])
    result = adaptive_qa_threshold(qa, min_valid_fraction=0.99)
    assert result == 0.0


@pytest.mark.parametrize("bad_fraction", [0.0, -0.5, 1.5])
def test_adaptive_threshold_rejects_invalid_fraction(bad_fraction):
    with pytest.raises(ValueError, match="min_valid_fraction"):
        adaptive_qa_threshold(np.array([0.5]), min_valid_fraction=bad_fraction)


def test_adaptive_threshold_rejects_empty_array():
    with pytest.raises(ValueError, match="empty"):
        adaptive_qa_threshold(np.array([]))


def test_kelvin_to_celsius_float_precision():
    result = kelvin_to_celsius(__import__("pandas").Series([273.15]))
    # pytest.approx handles float rounding gracefully
    assert result.iloc[0] == pytest.approx(0.0, abs=1e-9)


class TestKelvinConversion:
    """Grouping related tests in a class keeps things organized as a suite grows."""

    def test_normal_conversion(self, temperature_series):
        result = kelvin_to_celsius(temperature_series)
        assert result.iloc[0] == pytest.approx(0.0, abs=1e-6)

    def test_rejects_negative_kelvin(self):
        import pandas as pd

        with pytest.raises(ValueError, match="Negative Kelvin"):
            kelvin_to_celsius(pd.Series([-10.0]))
