import config
from flask import Flask, jsonify, request
from commands import ServerCommands

app = Flask(__name__)


def make_json_message(text: str):
    return jsonify({"message": f"{text}"})


def make_json_error(text: str):
    return jsonify({"error": f"{text}"})


@app.route("/system", methods=["GET"])
def system():
    info = ServerCommands.system()
    if info:
        return jsonify(info)
    else:
        return make_json_error("don't found system info")


@app.route("/shortcuts", methods=["GET"])
def shortcuts():
    info = ServerCommands.list_shortcuts()
    return jsonify(info)


@app.route("/applications", methods=["GET"])
def applications():
    info = ServerCommands.list_applications()

    if info:
        return jsonify(info)
    else:
        return make_json_error("don't found applications")


@app.route("/sound", methods=["POST"])
def sound():
    json = request.get_json(force=True)
    volume = json["volume"]
    if volume:
        ServerCommands.set_volume(volume)
    return make_json_message(f"Set volume: {volume}")


@app.route("/brightness", methods=["POST"])
def brightness_level():
    json = request.get_json(force=True)
    brightness = json["brightness_level"]

    if brightness is not None:
        ServerCommands.set_brightness(brightness)

    return make_json_message(f"Set brightness: {brightness}")


@app.route("/media", methods=["POST"])
def media():
    json = request.get_json(force=True)
    key = json["key"]

    if key:
        ServerCommands.press_key(key)

    return jsonify({"message": f"Pressed key: {key}"})


@app.route("/shortcut", methods=["POST"])
def run_shortcuts():
    json = request.get_json(force=True)
    shortcut = json["shortcut"]

    if shortcut:
        ServerCommands.run_shortcut(shortcut)

    return jsonify({"message": f"Run shortcut: {shortcut}"})


@app.route("/applications", methods=["POST"])
def close_application():
    json = request.get_json(force=True)
    application = json["application"]

    if application:
        ServerCommands.close_application(application)

    return make_json_message(f"close application: {application}")


if __name__ == '__main__':
    app.run(host=config.server_host, port=config.server_port)
