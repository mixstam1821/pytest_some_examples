"""
Marks: skip, skipif, xfail, and custom marks (e.g. 'slow') for selectively
running subsets of a large suite - useful to mention for CI pipelines.
"""
import sys

import pytest


@pytest.mark.skip(reason="Not implemented yet - placeholder for MTG LI L2 support")
def test_lightning_imager_l2_parsing():
    raise NotImplementedError


@pytest.mark.skipif(sys.platform == "win32", reason="HDF5 threading issue is Linux/macOS only")
def test_hdf5_thread_safety_behavior():
    assert True


@pytest.mark.xfail(reason="Known bug: reprojection south-up flip not yet fixed for this edge case")
def test_reprojection_edge_case_known_bug():
    assert False


@pytest.mark.slow
def test_large_dataset_processing():
    """
    Mark expensive tests as 'slow' so they can be excluded in fast CI runs
    with: pytest -m "not slow"
    """
    total = sum(range(10_000_000))
    assert total > 0
