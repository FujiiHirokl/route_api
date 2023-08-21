import numpy as np
import mysql.connector

def calculate_distance(point1, point2):
    return np.abs(np.linalg.norm(point1 - point2))



def trilateration(point1, point2, point3, d1, d2, d3):
    A = 2 * np.abs(point2 - point1)  # ベクトル A の計算
    B = 2 * np.abs(point3 - point1)  # ベクトル B の計算


    # 行列 C の計算
    C = d1**2 -  np.dot(point1, point1) - d2**2 + np.dot(point2, point2)


    # 行列 D 
    # の計算
    D = d1**2 - d3**2 - np.dot(point1, point1) + np.dot(point3, point3)

    print("ベクトル A:", A)
    print("ベクトル B:", B)
    print("行列 C:", C)
    print("行列 D:", D)

    # 行列方程式を解く
    coefficients = np.vstack((A, B)).T
    constants = np.array([C, D])
    point = np.linalg.solve(coefficients, constants)
    q,w = point
    if q > 0 and w > 0:
        point = (q, w)
    elif q > 0 and w < 0:
        point = (q,w*-1)
    elif q < 0 and w > 0:
        point = (q*-1,w)
    elif q < 0 and w < 0:
        point = (q*-1,w*-1)
        

    print("行列方程式の解:", point)

    return point


def get_device_coordinates(device_id):
    """指定されたデバイスIDに対応する座標情報をデータベースから取得します。

    Args:
        device_id (int): 取得したいデバイスのID。

    Returns:
        np.ndarray or None: デバイスの座標情報を含むNumPy配列。デバイスが見つからない場合はNone。
    """
    # MySQLデータベースへの接続
    connector = mysql.connector.connect(user='root', password='wlcm2T4', host='localhost', database='microphone', charset='utf8mb4')
    cursor = connector.cursor()
    
    select_query = "SELECT x_coordinate, y_coordinate FROM devices WHERE device_id = %s"
    cursor.execute(select_query, (device_id,))
    result = cursor.fetchone()  # デバイスIDに対応する座標情報を取得
    
    if result:
        x_coordinate, y_coordinate = result
        return np.array([x_coordinate, y_coordinate])
    else:
        return None
