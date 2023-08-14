from fastapi import FastAPI
from pydantic import BaseModel

class TaxIn(BaseModel):
    cost: int
    tax_rate: float

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello Masahiko"}

@app.post("/")
def calc(data: TaxIn):
    in_tax_cost = data.cost * (1 + data.tax_rate)
    return {'税込み価格': in_tax_cost}