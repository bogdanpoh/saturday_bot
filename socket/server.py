from flask import Flask, jsonify, request
from commands import ServerCommands

app = Flask(__name__)

tutorials = [
    {
        "title": "Video 1",
        "description": "GET, POST requests"
    },
    {
        "title": "Video 2",
        "description": "PUT, DELETE requests"
    }
]


@app.route("/system", methods=["GET"])
def system():
    info = ServerCommands().system()
    return jsonify(info)


@app.route("/", methods=["POST"])
def add_list():
    data = request.form
    tutorials.append(data)
    # print(jsonify(data).json)
    return jsonify(tutorials)


if __name__ == '__main__':
    app.run()
