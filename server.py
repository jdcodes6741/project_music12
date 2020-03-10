"""
Capital = class, functions = lowercase 
Flask = Need to import this because it is my application 
redirect = Used to redirect user to a different url (redirect for auth)
request = When a user talks to your site (visiting one of your routes, homepage
          or login. Their request information is going to be store inside the request object)
render_template = takes an html file and renders the actual html file the user will see
                  and gives it to a user/client
session = saving some values to the user/client's cookie (this is how we save the authentification token)

DebugToolbarExtension = renders the toolbar extension that we see on the right side of 
                        the screen 

requests = allows my server to make requests to other servers (like spotify) When you type in 
localhost5000, we are making a request to our server. My server sees this request, calls the 
homepage function, which returns an html page and return it

urllib = is a library that helps us with url related tasks (in this project, we will use the
urlencode function, which turns a dictionary into a query string)

"""
from flask import Flask, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import requests
import urllib

# app is an instance of the Flask class
# In order to use Flask SQLAlchemy, you need to have an app
app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

""" When we change the html page, the server automatically accounts for that change (need to refresh, but don't need to 
restart server) app.debug needs to be True in order for it to take effect """
app.jinja_env.auto_reload = True
app.secret_key="ABC"

# client id (my server)
SPOTIFY_CLIENT_ID="b51004b00f3841c4a5a7734a69c80576"
SPOTIFY_APP_SECRET="c543c3c9a49e41ed9da9712b2f01f20b"

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
    
    # Converts dictionary into query string
    # https://accounts.spotify.com/authorize?response_type=token&client_id=b51004b00f3841c4a5a7734a69c80576&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fauth%2Fcallback
    # urlencode converts space too
    query = urllib.parse.urlencode(params)
    return redirect(url+'?'+query)


# get spotify user code in order to create a token
@app.route('/auth/callback')
def auth():

    # request.args takes the parameters of a url and converts it into a dictionary
    #  How does it know what url to take? Spotify redirect returned a redirect_uri with a code that is unique 
    # to the user 
    params = request.args
    code = params["code"]

    # this is the url to get access_token from spotify
    url = "https://accounts.spotify.com/api/token"

    # payload is the body of the POST request. Spotify will need the information inside to determine if they should
    # give us an access token
    payload={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:5000/auth/callback",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_APP_SECRET,
    }

    # make the POST request which is composed of url and data we created earlier above
    # response object <response 200>
    response = requests.post(url, data=payload)


    # this is the response from spotify, and we converted it to a dictionary using .json()
    response_json = response.json()

    # return response_json

    # we extract the access token from the response
    access_token = response_json["access_token"]

    return redirect('/')

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    # run is an instance method
    app.run(host="0.0.0.0")
