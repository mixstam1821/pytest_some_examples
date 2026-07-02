# pytest examples

A small, self-contained repo demonstrating core pytest patterns against
domain code shaped like a real satellite-data pipeline (QA masking,
unit conversion, a fetch-from-remote-API function) plus a tiny FastAPI
service, similar in spirit to a backend like Xenia.

## Structure

```
src/
  pipeline.py   - domain functions under test (QA thresholding, masking, unit conversion, remote fetch)
  api.py        - a minimal FastAPI app
tests/
  conftest.py         - shared fixtures (sample xarray Dataset, pandas Series, FastAPI TestClient, session fixture)
  test_basics.py       - plain asserts, pytest.raises, pytest.approx, class-based grouping
  test_fixtures.py     - fixture usage, yield-fixtures (setup/teardown), tmp_path
  test_parametrize.py  - @pytest.mark.parametrize, including stacked parametrize
  test_mocking.py      - unittest.mock.patch and pytest's monkeypatch for external API calls
  test_api.py           - FastAPI endpoint testing with TestClient
  test_marks.py         - skip / skipif / xfail / custom marks (e.g. "slow")
pytest.ini             - marker registration and test discovery config
```

## What each file is meant to demonstrate in an interview

- **Fixtures & scopes** (`conftest.py`, `test_fixtures.py`): function vs
  session scope, yield-fixtures for setup/teardown, `tmp_path` for
  filesystem-touching tests without polluting the repo.
- **Parametrization** (`test_parametrize.py`): avoiding copy-pasted test
  functions, using `ids=` for readable output, stacking decorators for
  combinatorial coverage.
- **Mocking** (`test_mocking.py`): isolating tests from real network calls
  with both `unittest.mock.patch` and pytest's built-in `monkeypatch`,
  plus asserting on call arguments and simulating HTTP errors.
- **Exception & edge-case testing** (`test_basics.py`): `pytest.raises`
  with `match=`, boundary conditions (empty arrays, negative values).
- **API testing** (`test_api.py`): FastAPI's `TestClient`, status codes,
  404 handling.
- **Marks** (`test_marks.py`): `skip`, `skipif`, `xfail`, and a custom
  `slow` marker for selectively running subsets in CI (`pytest -m "not slow"`).

## Running

```bash
pip install -r requirements.txt
pytest                     # run everything
pytest -v                  # verbose
pytest -m "not slow"       # skip slow tests
pytest --cov=src           # with coverage, if pytest-cov is installed
```
