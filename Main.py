from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
# MySQLデータベースへの接続
connector = mysql.connector.connect(user='root', password='wlcm2T4', host='localhost', database='root', charset='utf8mb4')
cursor = connector.cursor()

class TaxIn(BaseModel):
    cost: int
    tax_rate: float
    
class CoordinateUpdate(BaseModel):
    device_id: int
    new_x: int
    new_y: int


app = FastAPI()

@app.get("/get_all_data")
def get_all_data():
    """全てのデータを取得するエンドポイント

    Returns:
        List[dict]: データベースから取得された結果のリスト
    """
    query = "SELECT * FROM route_data"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@app.get("/get_all_data_mame")
def get_all_data_mame():
    """経路名を取得するエンドポイント

    Returns:
        List[dict]: データベースから取得された経路名のリスト
    """
    query = "SELECT 経路名 FROM route_data"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@app.get("/get_route_data/{route_number}")
def get_route_data(route_number: int):
    """指定された経路番号のxとyを順番の順に取得するエンドポイント

    Args:
        route_number (int): 取得したい経路番号

    Returns:
        List[dict]: 指定された経路番号のxとyデータのリスト
    """
    query = f"SELECT x, y FROM route_data WHERE 経路番号 = {route_number} ORDER BY 順番"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@app.post("/")
def calc(data: TaxIn):
    """POSTリクエストを処理し、税込み価格を計算して返すエンドポイント

    Args:
        data (TaxIn): 計算に使用するデータ

    Returns:
        dict: 計算結果の辞書
    """
    in_tax_cost = data.cost * (1 + data.tax_rate)
    return {'税込み価格': in_tax_cost}

@app.get("/device_get")
def device_data():
    connector = mysql.connector.connect(user='root', password='wlcm2T4', host='localhost', database='microphone', charset='utf8mb4')
    cursor = connector.cursor()
    query = "SELECT * FROM devices"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connector.close()
    return result
    

@app.post("/update_coordinates")
def update_coordinates(data: CoordinateUpdate):
    """デバイスの座標を更新するエンドポイント

    Args:
        data (CoordinateUpdate): 更新する座標情報

    Returns:
        dict: 更新が成功したかどうかを示すメッセージ
    """
    connector = mysql.connector.connect(user='root', password='wlcm2T4', host='localhost', database='microphone', charset='utf8mb4')
    cursor = connector.cursor()

    update_query = "UPDATE devices SET x_coordinate = %s, y_coordinate = %s WHERE device_id = %s"
    cursor.execute(update_query, (data.new_x, data.new_y, data.device_id))
    connector.commit()

    cursor.close()
    connector.close()
    
    return {'message': f"デバイスID {data.device_id} の座標情報が更新されました。"}

