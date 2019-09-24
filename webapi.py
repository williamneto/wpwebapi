"""
Webapp flask que serve a API 

autor: William Neto <william.g.neto@gmail.com>
"""
from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory
from driver import WPWebAPI

app = Flask(__name__)
CORS(app)

wp_driver = WPWebAPI()


@app.route("/start_login", methods=["GET", "POST"])
def start_login():
    user = request.args.get("user") or request.form["user"]
    wp_driver.start(user)
    response = wp_driver.start_login(user)

    return jsonify(response)


@app.route("/close", methods=["GET", "POST"])
def close():
    user = request.args.get("user") or request.form["user"]
    response = wp_driver.close(user)
    return jsonify(response)


@app.route("/get_sended", methods=["GET", "POST"])
def get_sended():
    user = request.args.get("user") or request.form.get("user")
    message_id = request.args.get("message_id") or request.form.get("message_id")
    response = wp_driver.get_sended_message_status(user, message_id)

    return jsonify(response)


@app.route("/check_login", methods=["GET", "POST"])
def check_login():
    user = request.args.get("user") or request.form.get("user")
    response = wp_driver.check_login(user)

    return jsonify(response)


@app.route("/contacts", methods=["GET", "POST"])
def get_contacts():
    user = request.args.get("user") or request.form.get("user")
    response = wp_driver.get_contacts(user)

    return jsonify(response)


@app.route("/chats", methods=["GET", "POST"])
def get_all_chats():
    user = request.args.get("user")
    response = wp_driver.get_all_chats(user)

    return jsonify(response)


@app.route("/pic/<wpid>/", methods=["GET", "POST"])
def get_profile_pic(wpid):
    user = request.args.get("user")

    response = wp_driver.get_profile_pic(user, wpid)

    return jsonify(response)


@app.route("/chat/<id>/", methods=["GET", "POST"])
def get_chat(id):
    user = request.args.get("user")
    if request.args.get("limit"):
        response = wp_driver.get_chat(user, id, int(request.args.get("limit")))
    else:
        response = wp_driver.get_chat(user, id, 20)

    return jsonify(response)


@app.route("/send", methods=["GET", "POST"])
def send_message():
    user = request.args.get("user") or request.form.get("user")
    number = request.args.get("number") or request.form.get("number")
    message = request.args.get("message") or request.form.get("message")
    response = wp_driver.send_message(user, number, message)

    return jsonify(response)


@app.route("/send_media", methods=["GET", "POST"])
def send_media():
    user = request.args.get("user") or request.form.get("user")
    number = request.args.get("number") or request.form.get("number")
    url = request.args.get("url") or request.form.get("url")
    caption = request.args.get("caption") or request.form.get("caption")
    response = wp_driver.send_media(user, number, url, caption)

    return jsonify(response)


@app.route("/reg_sent", methods=["GET", "POST"])
def reg_sent():
    user = request.args.get("user") or request.form.get("user")
    chat_id = request.args.get("chat_id") or request.form.get("chat_id")

    response = wp_driver.reg_sent(user, chat_id)
    return jsonify(response)


@app.route("/delete_chat", methods=["GET", "POST"])
def delete_chat():
    user = request.args.get("user") or request.form.get("user")
    wpid = request.args.get("wpid") or request.form.get("wpid")

    response = wp_driver.delete_chat(user, wpid)

    return jsonify(response)


@app.route("/contacts_from_group", methods=["GET", "POST"])
def get_contacts_from_group():
    user = request.args.get("user") or request.form.get("user")

    response = wp_driver.get_contacts_from_groups(user)

    return jsonify(response)


@app.route("/check_number", methods=["GET", "POST"])
def check_number():
    user = request.args.get("user") or request.form.get("user")
    wpid = request.args.get("wpid") or request.form.get("wpid")

    response = wp_driver.check_number(user, wpid)

    return jsonify(response)


@app.route("/qrcodes/<path:path>")
def static_file(path):
    return send_from_directory("qrcodes/", path)


@app.route("/media/<path:path>")
def media_file(path):
    return send_from_directory("media/", path)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
