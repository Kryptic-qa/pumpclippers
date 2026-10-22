
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

    return """
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PUMPCLIPPERS - Verified</title>
</head>
<body style="background:#0b0b12; color:#f5f5f7; font-family:Arial,sans-serif; text-align:center; padding:60px 20px;">
  <h1 style="color:#b9ff39;">PUMPCLIPPERS</h1>
  <h2>TikTok Account Verified Successfully!</h2>
  <p style="color:#c5c5d0;">Your TikTok profile (user.info.basic) has been linked for clipping campaigns.</p>
  <p style="color:#888; font-size:12px;">Verification Auth ID: """ + code[:10] + """...</p>
  <a href="https://kryptic-qa.github.io/pumpclippers/" style="display:inline-block; margin-top:25px; background:#b9ff39; color:#0b0b12; padding:12px 24px; text-decoration:none; font-weight:bold; border-radius:6px;">Return to Dashboard</a>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
  
