from fastapi import FastAPI, HTTPException

app = FastAPI()

_FAKE_DB = {
    "MTG-FCI-001": {"instrument": "FCI", "status": "ready"},
    "S5P-SO2-002": {"instrument": "TROPOMI", "status": "processing"},
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/products/{product_id}")
def get_product(product_id: str):
    if product_id not in _FAKE_DB:
        raise HTTPException(status_code=404, detail="Product not found")
    return _FAKE_DB[product_id]
