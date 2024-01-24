from flask import Flask, request, Response
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import json
import requests
import os

app = Flask(__name__)
oauth = OAuth(app)

@app.get("/generatePlaylist")
def get_playlist() -> dict:
    print(request.args)
    if not spotify_client_id:
        return Response("invalid spotify client id, null value obtained!", status=500)
    if not spotify_client_secret:
        return Response("invalid spotify client secret, null value obtained!", status=500)
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

if __name__ == "__main__":
    # Let's test out OAuth2 with Spotify Account
    load_dotenv()
    spotify_access_token_url: str = "https://accounts.spotify.com/api/token"
    spotify_client_id: str = os.getenv['SPOTIFY_CLIENT_ID']
    assert spotify_client_id is not None
    spotify_client_secret: str = os.getenv['SPOTIFY_CLIENT_SECRET']
    assert spotify_client_secret is not None

    # Defining the OAuth2Session Object
    spotify_session = OAuth2Session()

    # app.run(debug=True)