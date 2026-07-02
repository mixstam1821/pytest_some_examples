"""
Small domain functions used to demonstrate testing patterns.
Mimics the kind of helpers you'd find in a satellite data pipeline:
QA masking, unit conversion, and fetching a remote product.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import xarray as xr
import requests


def adaptive_qa_threshold(qa: np.ndarray, min_valid_fraction: float = 0.1) -> float:
    """
    Pick the loosest QA threshold (from a fixed candidate list) that still
    keeps at least `min_valid_fraction` of pixels valid. Returns 0.0 if even
    the loosest threshold fails to reach the target (i.e. accept everything).
    """
    if not (0.0 < min_valid_fraction <= 1.0):
        raise ValueError("min_valid_fraction must be in (0, 1]")

    candidates = [0.75, 0.5, 0.25, 0.0]
    total = qa.size
    if total == 0:
        raise ValueError("qa array is empty")

    for threshold in candidates:
        valid_fraction = np.count_nonzero(qa >= threshold) / total
        if valid_fraction >= min_valid_fraction:
            return threshold
    return 0.0


def mask_dataset_by_qa(ds: xr.Dataset, qa_var: str, data_vars: list[str], threshold: float) -> xr.Dataset:
    """Mask `data_vars` (not coordinates!) below `threshold` on `qa_var`."""
    if qa_var not in ds:
        raise KeyError(f"{qa_var!r} not found in dataset")

    mask = ds[qa_var] >= threshold
    out = ds.copy()
    for var in data_vars:
        if var not in out:
            raise KeyError(f"{var!r} not found in dataset")
        out[var] = out[var].where(mask)
    return out


def kelvin_to_celsius(temp_k: pd.Series) -> pd.Series:
    if (temp_k < 0).any():
        raise ValueError("Negative Kelvin values are not physical")
    return temp_k - 273.15


def fetch_product_metadata(product_id: str, base_url: str = "https://api.example-eo.org") -> dict:
    """Fetch metadata for a satellite product from a remote API."""
    response = requests.get(f"{base_url}/products/{product_id}", timeout=10)
    response.raise_for_status()
    return response.json()
