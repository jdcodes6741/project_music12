from flask import Flask, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import requests
import urllib

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True
app.secret_key="ABC"

SPOTIFY_CLIENT_ID="b51004b00f3841c4a5a7734a69c80576"

# Homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')


# Login page which redirect to spotify
@app.route('/login')
def login():
    url = "https://accounts.spotify.com/authorize"
    params={
        "response_type": "code",
        "client_id": SPOTIFY_CLIENT_ID,
        "redirect_uri": "http://localhost:5000/auth/callback"
    }
    # request = requests.get(url=url, param=params)
    query = urllib.parse.urlencode(params)
    return redirect(url+'?'+query)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
