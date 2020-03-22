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

session = a global variable (look at flask sourcecode) Session object 


"""
from flask import Flask, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import requests
import urllib 
from model import User, connect_to_db, CountryPlaylist
import os

# app is an instance of the Flask class
# In order to use Flask SQLAlchemy, you need to have an app
app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

""" When we change the html page, the server automatically accounts for that change (need to refresh, but don't need to 
restart server) app.debug needs to be True in order for it to take effect """
app.jinja_env.auto_reload = True
app.secret_key="ABC"

# client id (my server)
SPOTIFY_CLIENT_ID= os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_APP_SECRET= os.getenv('SPOTIFY_APP_SECRET')


spotify_access_scopes = [
    "streaming",
    "user-read-email",
    "user-read-private",
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "app-remote-control",
]


# Homepage
@app.route('/')
def homepage():
    active_user = check_auth_and_fetch_current_user()
    
    return render_template('homepage.html', active_user=active_user)

# dynamic routing (placeholder <country_code>)
@app.route('/country_playlist/<country_code>')
def country_playlist(country_code):
    # check user's auth_token with our database to see if they are who they say they are or they need to login/create account
    active_user = check_auth_and_fetch_current_user()
    if not active_user:
        return redirect('/')

    # go to country_playlists table and use the country_code to find the playlist. If playlist not found, use the 
    # GLOBAL playlist.
    # playlist = store a country_playlist object (an instance)
    playlist = CountryPlaylist.query.get(country_code)
    if not playlist:
        playlist = CountryPlaylist.query.get('GLOBAL')

    # https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/
    # playlist is an instance. playlist_id is an attribute.
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist.playlist_id}"

    # https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/ (-H)
    # https://requests.readthedocs.io/en/master/user/quickstart/#make-a-request
    # every time we make a request to spotify, we have to include the access token in the header (according to Spotify's API)
    # get_auth_header() returns the header with the access token (this is needed for Spotify in order to verify the user has access)
    response = requests.get(playlist_url, headers=active_user.get_auth_header())

    if not response.ok:
        active_user.set_new_auth_token()
        active_user.save()
        return redirect("/")

    current_playlist = response.json()
    # return current_playlist
    return render_template('country_playlist.html', current_playlist=current_playlist, current_user=active_user)


# <> dynamic routing. When we have a request coming in, flask will look at the second part and pass in the items inside <> as a parameter
@app.route('/song/<song_id>')
def song(song_id):
    active_user = check_auth_and_fetch_current_user()
    if not active_user:
        return redirect('/')

    # https://developer.spotify.com/documentation/web-api/reference/tracks/get-track/
    # every time we make a request to spotify, we have to include the access token in the header (according to Spotify's API)
    song_url = f"https://api.spotify.com/v1/tracks/{song_id}"
    response = requests.get(song_url, headers=active_user.get_auth_header())

    if not response.ok:
        active_user.set_new_auth_token()
        active_user.save()
        return redirect("/")

    current_song = response.json()

    return render_template('song.html', current_song=current_song, current_user=active_user)


# Login page which redirect to spotify
@app.route('/login')
def login():
    url = "https://accounts.spotify.com/authorize"
    params={
        "response_type": "code",
        "client_id": SPOTIFY_CLIENT_ID,
        "redirect_uri": "http://localhost:5000/auth/callback",
        "scope": urllib.parse.quote(" ".join(spotify_access_scopes)),
    }
    
    # Converts dictionary into query string
    # https://accounts.spotify.com/authorize?response_type=token&client_id=b51004b00f3841c4a5a7734a69c80576&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fauth%2Fcallback
    # urlencode converts space too
    # redirect does not support passing in query params as a dictionary, we have to create a query string ourselves using 
    # urllib.parse.urlencode
    query = urllib.parse.urlencode(params)
    return redirect(url+'?'+query)


# get spotify user code in order to create a token
# auth/callback is only when a user logs in our app, once they log in, all subequent request will use the same access token
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

    print(response_json)
    # return response_json

    # we extract the access token from the response
    access_token = response_json["access_token"]

    # --------- End of token_access beyond this line -----------------

    headers = {'Authorization': f'Bearer {access_token}'}

    get_user_url = "https://api.spotify.com/v1/me"

    # Makes a get request to the first argument and pass in headers as a key argument
    ''' reponse https://developer.spotify.com/documentation/web-api/reference/users-profile/get-current-users-profile/
    will return a response object, need to convert it to a python dictionary
    '''
    response = requests.get(get_user_url, headers=headers)

    response_json = response.json()

    # return response_json

    spotify_id = response_json["id"]
    display_name = response_json["display_name"]

    active_user = User.query.get(spotify_id)


    # If the user is in our database, we assign them an access_token. If not, we create a new User instance 
    # Active user = logged in past, removed cookies, no access_token
    # lost auth_token = refresh token (I have your access_token and auth_token) as a user, I should also auth_token. User gives 
    # my app the auth_token. My app needs to verify the auth_token in my database (this is most likely judy), in this case, you need
    # to re-relog in (removed cookie)

    if active_user:
        active_user.access_token = access_token
    else:
        active_user =  User(spotify_id=spotify_id, display_name=display_name, access_token=access_token)

    # if not active_user:
    #     active_user =  User(spotify_id=spotify_id, display_name=display_name)

    # active_user.access_token = access_token

    # active_user.auth_token = token_urlsafe()
    active_user.set_new_auth_token()

    active_user.save()

    # auth token = browser to communicate to our server/app (for us to verify who the user is)
    # access token = our server/app to communicate with spotify API (for spotify to verify our server/app)

    # We can add keys to the session, which will update the user's cookie.
    # Every time the user makes a request, the auth_token is given back to the server and that is how the server 
    # check that row.
    # Can change display_name (spotify_id is unique)
    # Access_token = we dont want anyone to have it
    # Giving user these two information so that they can pass it back to us every subsequent request. 
    # session = to save the session on the browser.
    # Auth_token is for us to verify who the user is (every time the user clicks a different page, to prevent logging in everytime)
    session['auth_token'] = active_user.auth_token

    # assignment (updating the client's session)
    # stored auth_token and spotify_id in session. Session is stored on the client/browser. It is passed to the server 
    # on every request. That is how we can read from server.py
    session['spotify_id'] = spotify_id

    return redirect('/')


@app.route('/search')
def search():
    '''
        renders search page populated with songs from spotify
    '''
    # Not going to make a request to spotify until we know you are a real user. If user is not an active user, will return None
    active_user = check_auth_and_fetch_current_user()
    if not active_user:
        return redirect('/')

    # takes the query parameter from the url and turn it into a dictionary (included in the query parameter are keywords the user searched for in homepage.html)
    # {"q": "intentions"}
    params = request.args

    # return params

    # this "q" key matches the name="q" in homepage.html, want to get the "value" of what the user searched
    search_string = params["q"]

    # https://developer.spotify.com/documentation/web-api/reference/search/search/
    search_url = "https://api.spotify.com/v1/search"
    search_params = {
        "q": search_string,
        "type": "track",
        "limit": 20,
    }

    # every time we make a request to spotify, we have to include the access token in the header (according to Spotify's API)
    # example of what the request looks like: https://api.spotify.com/v1/search?q=intentions&type=track&limit=20
    response = requests.get(search_url, params=search_params, headers=active_user.get_auth_header())

    if not response.ok:
        active_user.set_new_auth_token()
        active_user.save()
        return redirect("/")

    # converts response object into a dictionary 
    search_items = response.json()

    # return search_items

    return render_template('search_page.html', search_string=search_string, search_items=search_items['tracks'], current_user=active_user)



# Only log in once, every other subsequent request, checks auth_token. This method is to check the user's auth_token.
def check_auth_and_fetch_current_user():
    # Anything in the session dictionary, we can see globally (if you have access to the session, you have all access to the information as well)
    if 'spotify_id' in session and "auth_token" in session:

        # We are storing the session["spotify_id"] into a variable called spotify_id
        spotify_id = session["spotify_id"]

        '''Database lives near server (database saves all information going on, historic online orders, only amazon has that information)
        We are saving all users who logged into our app in the Users table. 
        A user is making a request and giving me their spotify_id to tell me who they are. I need to check in my database if you logged in 
        After that is done,  there is a user with this spotify_id'''
        active_user = User.query.get(spotify_id)
        # value of session is encryted (auth_token and spotify_id is inside session)
        if active_user and active_user.auth_token == session["auth_token"]:
            return active_user



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    connect_to_db(app)

    # run is an instance method
    app.run(host="0.0.0.0")
