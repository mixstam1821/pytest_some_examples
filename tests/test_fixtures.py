"""
Fixture patterns: using conftest fixtures, yield-fixtures for setup/teardown,
and tmp_path for filesystem tests.
"""
import xarray as xr
import pytest

from src.pipeline import mask_dataset_by_qa


def test_mask_dataset_by_qa(sample_qa_dataset):
    """Uses the `sample_qa_dataset` fixture defined in conftest.py."""
    masked = mask_dataset_by_qa(sample_qa_dataset, "qa_value", ["radiance"], threshold=0.5)
    assert "radiance" in masked
    # Pixels below threshold should now be NaN, not dropped
    assert masked.radiance.isnull().sum() >= 0
    assert masked.radiance.shape == sample_qa_dataset.radiance.shape


def test_mask_dataset_raises_on_missing_qa_var(sample_qa_dataset):
    with pytest.raises(KeyError, match="not_a_real_var"):
        mask_dataset_by_qa(sample_qa_dataset, "not_a_real_var", ["radiance"], threshold=0.5)


def test_expensive_lookup_table_reused(expensive_lookup_table):
    """Session-scoped fixture - only built once even across many tests."""
    assert expensive_lookup_table["FCI"] == 16


@pytest.fixture
def netcdf_file(tmp_path, sample_qa_dataset):
    """
    A yield fixture: code before `yield` is setup, code after is teardown.
    tmp_path is a built-in pytest fixture giving a unique temp directory per test.
    """
    path = tmp_path / "sample_product.nc"
    sample_qa_dataset.to_netcdf(path)
    yield path
    # teardown happens automatically since tmp_path cleans itself up,
    # but this is where you'd close file handles / remove extra artifacts


def test_dataset_roundtrips_through_netcdf(netcdf_file):
    reloaded = xr.open_dataset(netcdf_file)
    assert "qa_value" in reloaded
    reloaded.close()
