from flask import Flask, request, redirect, url_for, current_app, abort, session, flash
from urllib.parse import urlencode
from dotenv import load_dotenv
import requests
import os
import secrets

load_dotenv()
app = Flask(__name__)
app.config["OAUTH2_PROVIDERS"] = {
    "spotify": {
        "client_id": os.environ.get("SPOTIFY_CLIENT_ID"),
        "client_secret": os.environ.get("SPOTIFY_CLIENT_SECRET"),
        "authorize_url": "https://accounts.spotify.com/authorize", 
        "token_url": "https://accounts.spotify.com/api/token",
        "scopes": ["playlist-read-private", "user-read-recently-played", "user-top-read", "playlist-modify-public"]
    }, 
    "apple-music": {

    }
}

@app.route("/authorize/<provider>")
def oauth2_authorize(provider):
    provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)
    session["oauth2_state"] = secrets.token_urlsafe(16)
    query_string = urlencode({
        "client_id": provider_data["client_id"],
        "redirect_uri": url_for("oauth2_callback", provider=provider, _external=True),
        "response_type": "code",
        "scope": " ".join(provider_data["scopes"]),
        "state": session["oauth2_state"]
    })
    return redirect(f"{provider_data['authorize_url']}?{query_string}")

@app.get("/callback/<provider>")
def oauth2_callback(provider):
    provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)
    if "error" in request.args:
        for key, val in request.args.items():
            if key.startswith("error"):
                flash(f"{key}: {val}")
        return redirect(url_for("index"))
    if request.args["state"] != session.get("oauth2_state") or "code" not in request.args:
        abort(401)
    response = requests.post(provider_data["token_url"], data={
        "client_id": provider_data["client_id"],
        "client_secret": provider_data["client_secret"],
        "code": request.args["code"],
        "grant_type": "authorization_code",
        "redirect_uri": url_for("oauth2_callback", provider=provider, _external=True)
    }, 
    headers={
        'Accept': 'application/json'
    })
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)
    current_app.config["OAUTH2_PROVIDERS"][provider]['access_token']

@app.route("/generatePlaylist")
def generate_playlist() -> dict:
    ...

if __name__ == "__main__":
    app.run(debug=True)