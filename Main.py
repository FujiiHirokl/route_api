from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
# MySQLデータベースへの接続
connector = mysql.connector.connect(user='root', password='wlcm2T4', host='localhost', database='root', charset='utf8mb4')
cursor = connector.cursor()

class TaxIn(BaseModel):
    cost: int
    tax_rate: float

app = FastAPI()

@app.get("/get_all_data")
def get_all_data():
    query = "SELECT * FROM route_data"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@app.post("/")
def calc(data: TaxIn):
    in_tax_cost = data.cost * (1 + data.tax_rate)
    return {'税込み価格': in_tax_cost}