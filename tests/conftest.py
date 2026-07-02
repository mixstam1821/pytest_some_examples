"""
Shared fixtures. Anything defined here is auto-discovered by pytest
and available in every test file without importing.
"""
import numpy as np
import pandas as pd
import pytest
import xarray as xr
from fastapi.testclient import TestClient

from src.api import app


@pytest.fixture
def sample_qa_dataset() -> xr.Dataset:
    """A small synthetic dataset shaped like a real satellite product."""
    rng = np.random.default_rng(seed=42)
    qa = rng.uniform(0, 1, size=(4, 4))
    radiance = rng.uniform(200, 300, size=(4, 4))
    return xr.Dataset(
        {
            "qa_value": (("y", "x"), qa),
            "radiance": (("y", "x"), radiance),
        }
    )


@pytest.fixture
def temperature_series() -> pd.Series:
    return pd.Series([273.15, 300.0, 250.0, 310.5], name="temp_k")


@pytest.fixture
def api_client() -> TestClient:
    """A fresh FastAPI TestClient per test."""
    return TestClient(app)


@pytest.fixture(scope="session")
def expensive_lookup_table() -> dict:
    """
    Session-scoped fixture: built once for the whole test run.
    Use for anything genuinely expensive (loading a big file, etc).
    """
    print("\n[building expensive_lookup_table once per session]")
    return {"FCI": 16, "TROPOMI": 7, "LI": 4}
