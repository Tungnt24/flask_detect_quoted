from flask import Flask, render_template, redirect, url_for, request
import json


app = Flask(__name__)


def load():
    with open("fake_data.json", "r") as f:
        data = json.load(f)
        return data

def get_quote(viewed_mail, received_mail):
    try:
        after_quote, quote, before_quote = received_mail.partition(viewed_mail)
        return quote
    except Exception:
        return ""

def get_viewed_folder(folder):
    if folder == "SENT":
        return "INBOX"
    return "SENT"

def get_user(user):
    if user == "A":
        return "B"
    return "A"


def insert(user, folder, message):
    data = load()
    with open("fake_data.json", "w") as f:
        data[user][0][folder] = message
        new_content = json.dumps(data, indent=4)
        f.write(new_content)


@app.route("/")
def main():
    data = load()
    sent = data['A'][0]["SENT"]
    inbox = data['A'][0]["INBOX"]
    sent_b = data['B'][0]["SENT"]
    inbox_b = data['B'][0]["INBOX"]
    quote = data["A"][0]['QUOTE']
    quote_b = data["B"][0]["QUOTE"]
    return render_template("index.html", sent=sent, inbox=inbox, sent_b=sent_b, inbox_b=inbox_b, quote=quote, quote_b=quote_b)


@app.route("/message", methods=["POST"])
def message():
    req = request.form.to_dict()
    user = req.get("user")
    message = req.get("message")
    folder = "SENT"
    insert(user, folder=folder, message=message)
    user = get_user(user)
    if user:
        folder = "INBOX"
        insert(user, folder, message)
    data = load()
    viewed = get_viewed_folder(folder)
    quote = get_quote(received_mail=message, viewed_mail=data[user][0][viewed])
    with open("fake_data.json", "w") as f:
        data[user][0]["QUOTE"] = quote
        new_quote = json.dumps(data, indent=4)
        f.write(new_quote)

    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=True, port=8000)