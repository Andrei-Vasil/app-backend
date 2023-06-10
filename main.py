import json
from flask import Flask, request
from flask_cors import CORS
from generate_request import generate_request
from process_request import process_request

app: Flask = Flask(__name__)
CORS(app)

@app.route("/random/<language>/<no_of_requests>/<request_size>", methods=['GET'])
def random(language, no_of_requests, request_size):
    print("WE IN BABY")
    try:
        response = process_request(language, generate_request(int(request_size)), int(no_of_requests))
        return json.dumps(response), 200
    except Exception as e:
        print(e)
        return f'{str(e)}\r\n', 404

@app.route("/custom/<language>/<no_of_requests>", methods=['POST'])
def custom(language, no_of_requests):
    try:
        response = process_request(language, request.json['request'], int(no_of_requests))
        return json.dumps(response), 200
    except Exception as e:
        print(e)
        return f'{str(e)}\r\n', 404


if __name__ == "__main__":
    app.run(port=24511)
