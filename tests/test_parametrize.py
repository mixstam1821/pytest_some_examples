"""
Parametrization: run the same test logic against many inputs without
duplicating code. This is what interviewers usually want to see first.
"""
import numpy as np
import pytest

from src.pipeline import adaptive_qa_threshold


@pytest.mark.parametrize(
    "qa_values, min_fraction, expected",
    [
        (np.array([0.9, 0.9, 0.9, 0.9]), 0.5, 0.75),
        (np.array([0.6, 0.6, 0.1, 0.1]), 0.5, 0.5),
        (np.array([0.1, 0.1, 0.1, 0.1]), 0.5, 0.0),
    ],
    ids=["all-high-qa", "mixed-qa", "all-low-qa"],
)
def test_threshold_selection_matrix(qa_values, min_fraction, expected):
    assert adaptive_qa_threshold(qa_values, min_fraction) == expected


# Stacking two parametrize decorators multiplies the cases (3 x 2 = 6 runs)
@pytest.mark.parametrize("min_fraction", [0.25, 0.75])
@pytest.mark.parametrize("size", [4, 16, 64])
def test_threshold_selection_scales_with_array_size(size, min_fraction):
    qa = np.linspace(0, 1, size)
    result = adaptive_qa_threshold(qa, min_fraction)
    assert result in [0.75, 0.5, 0.25, 0.0]


@pytest.mark.parametrize("product_id", ["MTG-FCI-001", "S5P-SO2-002"])
def test_known_products_exist(api_client, product_id):
    response = api_client.get(f"/products/{product_id}")
    assert response.status_code == 200
