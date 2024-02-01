var express = require("express");
const { abort } = require("process");
var router = express.Router()

const providerConfig = {
    "spotify": {
        "clientId": process.env.SPOTIFY_CLIENT_ID,
        "clientSecret": process.env.SPOTIFY_CLIENT_SECRET,
        "authorizeUrl": "https://accounts.spotify.com/authorize", 
        "tokenUrl": "https://accounts.spotify.com/api/token",
        "scopes": ["playlist-read-private", "user-read-recently-played", "user-top-read", "playlist-modify-public"]
    }, 
    "appleMusic": {},
    "youtubeMusic": {}
}

router.get("/:provider", function(req, res, next) {
    const provider = req.params["provider"]
    if (provider.trim().length === 0) {
        console.log("clapped")
        next("error")
    }

});