import json
 
def load():
    with open("fake_data.json", "r") as f:
        data = json.load(f)
        return data


def get_quoted(viewed_mail, received_mail):
    try:
        after_quote, quote, before_quote = received_mail.partition(viewed_mail)
        if quote != "":
            return quote

        words = viewed_mail.split()
        quote_raw = [word for word in words if word in received_mail]
        quote = " ".join(quote_raw)
        if quote == viewed_mail:
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