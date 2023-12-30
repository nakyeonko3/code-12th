from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from user_data_management import UserDataManagement
import subprocess
import json

app = Flask(__name__)
CORS(app)

user_data_management = UserDataManagement()

@app.route("/UserInfo", methods=["POST"])
def handle_user():
    data = request.json
    EventID = data.get("EventID")

    if EventID == "1":
        UserData = {
            "Name": data.get("Name"),
            "CarType": data.get("CarType"),
            "CarNumber": data.get("CarNumber"),
        }

        # C 프로그램 실행
        result = subprocess.run(["/home/ctj/projects/Project/Cuser_data", UserData["Name"], UserData["CarType"], UserData["CarNumber"]], capture_output=True, text=True)

        if result.returncode == 0:
            print("C 프로그램의 출력: ", result.stdout)
            response_data = {"message": "데이터가 등록되었습니다."}
            return Response(json.dumps(response_data, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8')
        else:
            response_data = {"message": "C 프로그램 실행 중 오류가 발생했습니다."}
            return Response(json.dumps(response_data, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8')

    elif EventID == "2":
        ParkingSpace = {
            "ParkingSpace": data.get("ParkingSpace"),
            "CarNumber": data.get("CarNumber"),
        }

        # match_and_register_data 함수를 호출하고 반환값을 result에 저장
        result = user_data_management.match_and_register_data(ParkingSpace["CarNumber"], ParkingSpace["ParkingSpace"])

        if result == "주차 공간이 등록되었습니다.":
            response_data = {"message": result}
        else:
            response_data = {"message": "주차 공간이 등록되지 않았습니다."}

        response = Response(json.dumps(response_data, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8')

    return response


@app.route("/get-json-data", methods=["GET"])
def get_json_data():

    EventID = request.args.get("EventID")
    
    # 클라이언트로부터 받은 EventID 출력
    print(f"Received EventID from client: {EventID}")
    
    if EventID == "3":
        result = subprocess.run(["./Rmap_data"], capture_output = True, text = True, cwd = "/home/ctj/projects/Project")
        if result.returncode == 0:
            print("returncode: ", result.returncode)
            json_data = result.stdout # stdout: Standard Output 줄임말, "./Rmap_data" 실행하고 저장하고 반환합니다.
            print("Command Output: ", result.stdout)
            return jsonify(json_data)
        else:
            return jsonify({"message": "데이터가 없습니다."}), 404 # 클라이언트가 요청한 데이터를 서버에서 찾을 수 없는 오류입니다.
    else:
        return jsonify({"message": "잘못된 EventID입니다."}), 404 # 클라이언트가 요청한 데이터를 서버에서 찾을 수 없는 오류입니다.

if __name__ == "__main__":
    app.run(host = "0.0.0.0")