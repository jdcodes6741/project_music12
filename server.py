from flask import Flask, redirect, request, render_template, session, flash
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
    
    return render_template('homepage.html', current_user=active_user)


@app.route('/country_playlist/<country_code>')
def country_playlist(country_code):
    active_user = check_auth_and_fetch_current_user()
    if not active_user:
        flash('Session expired. Please login again.')
        return redirect('/')

    # go to country_playlists table and use the country_code to find the playlist. If playlist not found, use the 
    # GLOBAL playlist.
    playlist = CountryPlaylist.query.get(country_code)
    if not playlist:
        playlist = CountryPlaylist.query.get('GLOBAL')


    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist.playlist_id}"

    # need to include the access token in the header 
    response = requests.get(playlist_url, headers=active_user.get_auth_header())

    if not response.ok:
        active_user.set_new_auth_token()
        active_user.save()
        return redirect("/")

    current_playlist = response.json()
    # return current_playlist
    return render_template('country_playlist.html', current_playlist=current_playlist, current_user=active_user)


# When we have a request coming in, flask will look at the second part and pass in the items inside <> as a parameter
@app.route('/song/<song_id>')
def song(song_id):
    active_user = check_auth_and_fetch_current_user()
    if not active_user:
        flash('Session expired. Please login again.')
        return redirect('/')

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
    query = urllib.parse.urlencode(params)
    return redirect(url+'?'+query)

@app.route('/logout')
def logout():
    active_user = check_auth_and_fetch_current_user()
    if active_user:
        active_user.set_new_auth_token()
        active_user.save()

    return redirect("/")


@app.route('/auth/callback')
def auth():

    # request.args takes the parameters of a url and converts it into a dictionary
    params = request.args
    code = params["code"]

    url = "https://accounts.spotify.com/api/token"

    payload={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:5000/auth/callback",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_APP_SECRET,
    }

    # response object <response 200>
    response = requests.post(url, data=payload)


    # this is the response from spotify, and we converted it to a dictionary using .json()
    response_json = response.json()

    # print(response_json)
    # return response_json

    access_token = response_json["access_token"]

    # --------- End of token_access beyond this line -----------------

    headers = {'Authorization': f'Bearer {access_token}'}

    get_user_url = "https://api.spotify.com/v1/me"

    response = requests.get(get_user_url, headers=headers)

    response_json = response.json()

    # return response_json

    spotify_id = response_json["id"]
    display_name = response_json["display_name"]

    active_user = User.query.get(spotify_id)


    # If the user is in our database, we assign them an access_token. If not, we create a new User instance 
    # Active user = logged in past, removed cookies, no access_token
    # lost auth_token = refresh token (I have your access_token and auth_token) as a user, I should also auth_token. User gives 
    # my app the auth_token. My app needs to verify the auth_token in my database, in this case, you need
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

    session['auth_token'] = active_user.auth_token

    # assignment (updating the client's session)
    # stored auth_token and spotify_id in session. Session is stored on the client/browser. It is passed to the server 
    # on every request. That is how we can read from server.py
    session['spotify_id'] = spotify_id

    flash('You were successfully logged in')
    return redirect('/')


@app.route('/search')
def search():
    '''
        renders search page populated with songs from spotify
    '''
    # Not going to make a request to spotify until we know you are a real user. If user is not an active user, will return None
    active_user = check_auth_and_fetch_current_user()
    if not active_user:
        flash('Session expired. Please login again.')
        return redirect('/')

    # takes the query parameter from the url and turn it into a dictionary (included in the query parameter are keywords the user searched for in homepage.html)
    # {"q": "intentions"}
    params = request.args

    # return params

    # this "q" key matches the name="q" in homepage.html, want to get the "value" of what the user searched
    search_string = params["q"]

    search_url = "https://api.spotify.com/v1/search"
    search_params = {
        "q": search_string,
        "type": "track",
        "limit": 20,
    }

    response = requests.get(search_url, params=search_params, headers=active_user.get_auth_header())

    if not response.ok:
        active_user.set_new_auth_token()
        active_user.save()
        return redirect("/")

    # converts response object into a dictionary 
    search_items = response.json()

    # return search_items

    return render_template('search_page.html', search_string=search_string, search_items=search_items['tracks'], current_user=active_user)



def check_auth_and_fetch_current_user():
    # Anything in the session dictionary, we can see globally (if you have access to the session, you have all access to the information as well)
    if 'spotify_id' in session and "auth_token" in session:

        spotify_id = session["spotify_id"]

        active_user = User.query.get(spotify_id)

        if active_user and active_user.auth_token == session["auth_token"]:
            return active_user



if __name__ == "__main__":
    DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(host="0.0.0.0")
