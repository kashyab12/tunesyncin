from flask import Flask, request, Response, redirect
from urllib.parse import urlencode
from dotenv import load_dotenv
import json
import requests
import os
import random
import string
import base64

app = Flask(__name__)

# Global dict to store important info
request_vars = {}

@app.get("/authorize")
def authorize() -> None:
    csrf_token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    request_vars[csrf_token] = {
        "client_id": request.args.get('client_id'),
        "client_secret": request.args.get('client_secret'),
        "scope": "playlist-read-private user-read-recently-played user-top-read playlist-modify-public",
        "redirect_uri": "http://localhost:5000/callback/spotify"
    }
    redirect_params = {
        "client_id": request_vars[csrf_token]["client_id"],
        "scope": request_vars[csrf_token]["scope"],
        "response_type": "code",
        "redirect_uri": request_vars[csrf_token]["redirect_uri"],
        "state": csrf_token 
    }
    redirect_url = f"https://accounts.spotify.com/authorize?{urlencode(redirect_params, doseq=True)}"
    return redirect(redirect_url)

@app.get("/callback/spotify")
def spotify_callback() -> None:
    print("Awesome! We have reached here")
    if request.args.get("error") is not None:
        # TODO: Handle the error
        ...
    else:
        access_code = request.args.get("code")
    csrf_token = request.args.get("state")
    if csrf_token not in request_vars:
        # TODO: Abort mission!
        ...
    grant_type = "authorization_code"
    header_auth = base64.b64encode(f"{request_vars[csrf_token]['client_id']}:{request_vars[csrf_token]['client_secret']}".encode())
    header_content_type = "application/x-www-form-urlencoded"
    request_body = {
        "code": access_code,
        "redirect_uri": request_vars[csrf_token]["redirect_uri"],
        "grant_type": grant_type
    }
    request_header = {
        "content_type": header_content_type,
        "Authorization": f"Basic: {str(header_auth)}"
    }
    # TODO: Invalid client and 400 response?
    resp = requests.post("https://accounts.spotify.com/api/token", data=request_body, headers=request_header)
    assert resp.status_code == 200
    return redirect("localhost:5000/generatePlaylist")


@app.get("/generatePlaylist")
def get_playlist() -> dict:
    print(request.args)
    # if not spotify_client_id:
    #     return Response("invalid spotify client id, null value obtained!", status=500)
    # if not spotify_client_secret:
    #     return Response("invalid spotify client secret, null value obtained!", status=500)
    # user1: str = request.args["user1"] 
    # spotify_access_token_data: dict = {
    #     "grant_type": "client_credentials", 
    #     "client_id": spotify_client_id, 
    #     "client_secret": spotify_client_secret
    # }
    # spotify_acc_tok_req: requests.Response = requests.post(spotify_access_token_url, data=spotify_access_token_data)
    # assert spotify_acc_tok_req.status_code == 200, f"Received {spotify_acc_tok_req.status_code} status code upon querying spotify for an access code!"
    # spotify_access_token: str = spotify_acc_tok_req.json().get("access_token")
    # return spotify_access_token

if __name__ == "__main__":
    app.run(debug=True)