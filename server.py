from flask import Flask, request
import json
import requests
import os

spotify_access_token_url: str = "https://accounts.spotify.com/api/token"
spotify_client_id: str = os.environ['SPOTIFY_CLIENT_ID']
spotify_client_secret: str = os.environ['SPOTIFY_CLIENT_SECRET']

app = Flask(__name__)

@app.get("/generatePlaylist")
def get_playlist() -> dict:
    print(request.args)
    assert len(spotify_client_id) > 0, "Invalid spotify client id, null value obtained!"
    assert len(spotify_client_secret) > 0, "Invalid spotify client secret, null value obtained!"
    user1: str = request.args["user1"] 
    spotify_access_token_data: dict = {
        "grant_type": "client_credentials", 
        "client_id": spotify_client_id, 
        "client_secret": spotify_client_secret
    }
    spotify_acc_tok_req: requests.Response = requests.post(spotify_access_token_url, data=spotify_access_token_data)
    assert spotify_acc_tok_req.status_code == 200, f"Received {spotify_acc_tok_req.status_code} status code upon querying spotify for an access code!"
    spotify_access_token: str = spotify_acc_tok_req.json().get("access_token")
    return spotify_access_token