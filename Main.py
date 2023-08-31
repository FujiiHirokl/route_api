
# ファイル: Main.py
# 作成者: 藤井広輝
# 更新日: 2023/8/28
# 説明: AGVプログラムで扱うAPI

# 必要なライブラリをインポート
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import os

db_pass = os.getenv('db_pass')

# 環境変数が設定されていない場合のデフォルト値
default_db_pass = 'default_password'

# データベースパスワードが存在しない場合、デフォルト値を使用
if db_pass is None:
    db_pass = default_db_pass
    
# 自作モジュールから必要な部分をインポート
from potision_sum import calculate_distance, trilateration,get_device_coordinates

    # TaxInクラス: 計算に使用するデータモデル
class TaxIn(BaseModel):
    cost: int         # 商品の原価
    tax_rate: float   # 税率

# CoordinateUpdateクラス: デバイスの座標を更新するためのデータモデル
class CoordinateUpdate(BaseModel):
    device_id: int    # デバイスID
    new_x: int        # 新しいX座標
    new_y: int        # 新しいY座標

# CoordinatesInputクラス: 測定データから位置座標を推定するためのデータモデル
class CoordinatesInput(BaseModel):
    d1: float         # 測定データ1
    d2: float         # 測定データ2
    d3: float         # 測定データ3
    d4: float         # 測定データ4

class coordinate_position(BaseModel):
    coordinate_position_x: int  #格納座標
    coordinate_position_y: int  #格納座標
    


app = FastAPI()

@app.get("/get_all_data")
def get_all_data():
    """全てのデータを取得するエンドポイント

    Returns:
        List[dict]: データベースから取得された結果のリスト
    """
    try:
        connector = mysql.connector.connect(user='root', password=db_pass, host='localhost', database='root', charset='utf8mb4')
        cursor = connector.cursor()
        query = "SELECT * FROM route_data"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        return {"error" : str(e)}

@app.get("/get_all_data_mame")
def get_all_data_mame():
    """経路名を取得するエンドポイント

    Returns:
        List[dict]: データベースから取得された経路名のリスト
    """
    try:
        connector = mysql.connector.connect(user='root', password=db_pass, host='localhost', database='root', charset='utf8mb4')
        cursor = connector.cursor()
        query = "SELECT 経路名 FROM route_data"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        return {"error" : str(e)}

@app.get("/get_route_data/{route_number}")
def get_route_data(route_number: int):
    """指定された経路番号のxとyを順番の順に取得するエンドポイント

    Args:
        route_number (int): 取得したい経路番号

    Returns:
        List[dict]: 指定された経路番号のxとyデータのリスト
    """
    try:
        connector = mysql.connector.connect(user='root', password=db_pass, host='localhost', database='root', charset='utf8mb4')
        cursor = connector.cursor()
        query = f"SELECT x, y FROM route_data WHERE 経路番号 = {route_number} ORDER BY 順番"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        return {"error" : str(e)}

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
    """マイクの情報を取得する

    Returns:
        _type_: _description_
    """
    try:
        connector = mysql.connector.connect(user='root', password=db_pass, host='localhost', database='microphone', charset='utf8mb4')
        cursor = connector.cursor()
        query = "SELECT * FROM devices"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connector.close()
        return result
    except Error as e:
        return {"error" : str(e)}
    

@app.post("/update_coordinates")
def update_coordinates(data: CoordinateUpdate):
    """デバイスの座標を更新するエンドポイント

    Args:
        data (CoordinateUpdate): 更新する座標情報

    Returns:
        dict: 更新が成功したかどうかを示すメッセージ
    """
    try:
        connector = mysql.connector.connect(user='root', password=db_pass, host='localhost', database='microphone', charset='utf8mb4')
        cursor = connector.cursor()

        update_query = "UPDATE devices SET x_coordinate = %s, y_coordinate = %s WHERE device_id = %s"
        cursor.execute(update_query, (data.new_x, data.new_y, data.device_id))
        connector.commit()

        cursor.close()
        connector.close()
        
        return {'message': f"デバイスID {data.device_id} の座標情報が更新されました。"}
    except Error as e:
        return {"error" : str(e)}
    
@app.post("/math_coordinates")
def update_coordinates(data: CoordinatesInput):
    """測定データから位置座標を推定するエンドポイント

    Args:
        data (CoordinatesInput): 測定データを含むモデル。d1, d2, d3, d4 が必要です。

    Returns:
        dict: 推定された位置座標
    """

    # 測定ポイントの座標をリストにまとめる
    points = [get_device_coordinates(i) for i in range(1, 5)]

    # 測定ポイントからの距離をリストにまとめる
    distances = [data.d1, data.d2, data.d3, data.d4]

    # 結果を格納するリストを初期化
    results = []

    # 各セットのトライアングレーションと距離の計算を行い、結果をリストに追加
    for i in range(4):
        next_i = (i + 1) % 4
        next_next_i = (next_i + 1) % 4

        result = trilateration(points[i], points[next_i], points[next_next_i],
                               distances[i], distances[next_i], distances[next_next_i])
        result_value = calculate_distance(calculate_distance(result, points[i]), distances[i]) + \
                       calculate_distance(calculate_distance(result, points[next_i]), distances[next_i]) + \
                       calculate_distance(calculate_distance(result, points[next_next_i]), distances[next_next_i])

        results.append(result_value)

    # 最小の結果を取得
    min_result = min(results)

    return {
        "estimated_position": min_result
    }

@app.post("/update_Coordinate") 
def update_Coordinate(date: coordinate_position):
    """
    座標を更新するエンドポイントです。

    Args:
        date (coordinate_position): 更新する座標の情報が含まれたデータ

    Returns:
        dict: 更新が成功した場合は成功メッセージ、エラーが発生した場合はエラーメッセージ
    """
    try:
        # データベースに接続
        connector = mysql.connector.connect(user='root', password=db_pass, host='localhost', database='root', charset='utf8mb4')
        cursor = connector.cursor()
        
        # UPDATEクエリの作成と実行
        update_query = "UPDATE coordinates SET x = %s, y = %s WHERE id = 1"
        cursor.execute(update_query, (date.coordinate_position_x, date.coordinate_position_y))
        connector.commit()
        
        # リソースを解放
        cursor.close()
        connector.close()
        
        # 成功メッセージを返す
        return {"message": "x座標 " + str(date.coordinate_position_x) + " および y座標 " + str(date.coordinate_position_y) + " を格納しました"}
    
    except Error as e:
        # エラーメッセージを返す
        return {"error": str(e)}
    
@app.get("/Get_position_coordinates")
def Get_position_coordinates():
    """
    座標を取得するエンドポイントです。

    Returns:
        dict: 座標情報
    """
    try:
        # データベースに接続
        connector = mysql.connector.connect(user='root', password=db_pass, host='localhost', database='root', charset='utf8mb4')
        cursor = connector.cursor()
        
        # SELECTクエリの作成と実行
        select_query = "SELECT x, y FROM coordinates WHERE id = 1;"
        cursor.execute(select_query)
        
        # 結果の取得
        result = cursor.fetchone()
        
        # リソースを解放
        cursor.close()
        connector.close()
        
            # 結果を返す
        return {"message": "x座標 " + str(result[0]) + " および y座標 " + str(result[1]) + " を格納しました"}
    
    except Error as e:
        # エラーメッセージを返す
        return {"error": str(e)}