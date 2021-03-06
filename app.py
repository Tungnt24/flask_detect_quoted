from flask import Flask, render_template, redirect, url_for, request
import json
from crud import *


app = Flask(__name__)



@app.route("/")
def main():
    data = load()
    sent = data["A"][0]["SENT"]
    inbox = data["A"][0]["INBOX"]
    sent_b = data["B"][0]["SENT"]
    inbox_b = data["B"][0]["INBOX"]
    quote_a_inbox = data["A"][0]["QUOTE_INBOX"]
    quote_b_inbox = data["B"][0]["QUOTE_INBOX"]
    quote_a_sent = data["A"][0]["QUOTE_SENT"]
    quote_a_sent2 = data["A"][0]["QUOTE_SENT2"]
    quote_b_sent = data["B"][0]["QUOTE_SENT"]
    quote_b_sent2 = data["B"][0]["QUOTE_SENT2"]
    return render_template(
        "index.html",
        sent=sent,
        inbox=inbox,
        sent_b=sent_b,
        inbox_b=inbox_b,
        quote_a_inbox=quote_a_inbox,
        quote_b_inbox=quote_b_inbox,
        quote_a_sent=quote_a_sent,
        quote_a_sent2=quote_a_sent2,
        quote_b_sent=quote_b_sent,
        quote_b_sent2=quote_b_sent2,
    )


@app.route("/message", methods=["POST"])
def message():
    req = request.form.to_dict()
    user = req.get("user")
    message = req.get("message")

    insert(user, folder="SENT", message=message)
    insert(user, folder="QUOTE_SENT2", message=message)

    data = load()
    user = get_user(user)

    insert(user, folder="INBOX", message=message)
    insert(user, folder="QUOTE_SENT", message=message)

    seen = data[user][0]["SENT"]
    if seen == "":
        seen = data[user][0]["INBOX"]

    quote = get_quoted(received_mail=message, viewed_mail=seen)
    insert(user, folder="QUOTE_INBOX", message=quote)

    return redirect(url_for("main"))


@app.route("/reset", methods=["POST"])
def reset():
    data = load()
    with open("fake_data.json", "w") as f:
        data = {
            "A": [
                {
                    "SENT": "",
                    "QUOTE_SENT": "",
                    "QUOTE_SENT2": "",
                    "INBOX": "",
                    "QUOTE_INBOX": "",
                }
            ],
            "B": [
                {
                    "SENT": "",
                    "QUOTE_SENT": "",
                    "QUOTE_SENT2": "",
                    "INBOX": "",
                    "QUOTE_INBOX": "",
                }
            ],
        }
        new_data = json.dumps(data, indent=4)
        f.write(new_data)
        return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=True, port=8000)
