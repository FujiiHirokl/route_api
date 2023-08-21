import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import mysql.connector

# MySQLデータベースへの接続
connector = mysql.connector.connect(user='root', password='wlcm2T4', host='localhost', database='root', charset='utf8mb4')
cursor = connector.cursor()


distance_age = 0
i = 0

def get_device_coordinates(device_id):
    select_query = "SELECT x_coordinate, y_coordinate FROM devices WHERE device_id = %s"
    cursor.execute(select_query, (device_id,))
    result = cursor.fetchone()  # デバイスIDに対応する座標情報を取得
    if result:
        x_coordinate, y_coordinate = result
        return np.array([x_coordinate, y_coordinate])
    else:
        return None




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

# 測定ポイントの座標
# 特定のデバイスIDを入力して座標情報を取得

# 測定ポイントの座標
point1 = np.array([10, 10])
point2 = np.array([10, 490])
point3 = np.array([490, 10])
point4 = np.array([490,490])



x = float(input("X座標を入力してください: "))
y = float(input("Y座標を入力してください: "))
clicked_position = np.array([x, y])
    
print(clicked_position)
    
# 測定ポイントからの距離にランダムなブレを加える
d1 = np.linalg.norm(clicked_position - point1) + np.random.normal(-20, 20)
d2 = np.linalg.norm(clicked_position - point2) + np.random.normal(-20, 20)
d3 = np.linalg.norm(clicked_position - point3) + np.random.normal(-20, 20)
d4 = np.linalg.norm(clicked_position - point4) + np.random.normal(-20, 20)
    
# 3点測位の実行
result = trilateration(point1, point2, point3, d1, d2, d3)
result_value = calculate_distance(calculate_distance(result, point1), d1) + calculate_distance(calculate_distance(result, point2), d2) + calculate_distance(calculate_distance(result, point3), d3)

result2 = trilateration(point2, point3, point4, d2, d3, d4)
result2_value = calculate_distance(calculate_distance(result2, point2), d2) + calculate_distance(calculate_distance(result2, point3), d3) + calculate_distance(calculate_distance(result2, point4), d4)

result3 = trilateration(point3, point4, point1, d3, d4, d1)
result3_value = calculate_distance(calculate_distance(result3, point1), d1) + calculate_distance(calculate_distance(result3, point3), d3) + calculate_distance(calculate_distance(result3, point4), d4)

result4 = trilateration(point4, point1, point2, d4, d1, d2)
result4_value = calculate_distance(calculate_distance(result4, point1), d1) + calculate_distance(calculate_distance(result4, point2), d2) + calculate_distance(calculate_distance(result4, point4), d4)

min_result = min(result_value, result2_value, result3_value, result4_value)

# 結果の表示s
print("推定された位置座標:", result)
print("推定された位置座標:", result2)
print("推定された位置座標:", result3)
print("推定された位置座標:", result4)
    
    
# クリックした点と求められた座標の距離を出力
distance = np.linalg.norm(clicked_position - result)
print("クリックした点と推定された座標の距離:", distance)
distance = np.linalg.norm(clicked_position - result2)
print("クリックした点と推定された座標の距離:", distance)
distance = np.linalg.norm(clicked_position - result3)
print("クリックした点と推定された座標の距離:", distance)
distance = np.linalg.norm(clicked_position - result4)
print("クリックした点と推定された座標の距離:", distance)
    
if min_result == result_value:
    print("Minimum value is from result:", result)
elif min_result == result2_value:
    print("Minimum value is from result2:", result2)
elif min_result == result3_value:
    print("Minimum value is from result3:", result3)
else:
    print("Minimum value is from result4:", result4)
        