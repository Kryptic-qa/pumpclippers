
import os
import secrets
import urllib.parse

from flask import Flask, request, redirect

app = Flask(__name__)

CLIENT_KEY = os.environ.get("TIKTOK_CLIENT_KEY")

REDIRECT_URI = "https://pumpclippers.onrender.com/callback"


@app.route("/")
def home():
    return "PumpClippers TikTok server is running."


@app.route("/login")
def login():
    if not CLIENT_KEY:
        return "Missing TikTok Client Key", 500

    state = secrets.token_urlsafe(24)

    params = {
        "client_key": CLIENT_KEY,
        "response_type": "code",
        "scope": "user.info.basic",
        "redirect_uri": REDIRECT_URI,
        "state": state,
    }

    url = (
        "https://www.tiktok.com/v2/auth/authorize/?"
        + urllib.parse.urlencode(params)
    )

    return redirect(url)


@app.route("/callback")
def callback():
    error = request.args.get("error")
    code = request.args.get("code")

    if error:
        return f"TikTok authorization failed: {error}", 400

    if not code:
        return "Authorization code not received.", 400

    return (
        "TikTok authorization received. "
        "Token exchange is not implemented yet."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
  
