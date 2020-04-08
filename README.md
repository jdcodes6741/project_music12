# Globify

Project diagram & Data Model:
https://docs.google.com/presentation/d/10SvQfrefrNFBLIw8qo2vyjCyGZOkRd3vljbEJ_eeo2Y/edit?usp=sharing


User Story: Music is the universal language of mankind. As an avid music lover, I love listening to all types of music, especially in different languages. Music is universal and you don’t really need to understand the lyrics to a song in order to like it. Most of the time, songs are in English and I still don’t understand the lyrics. Globally, songs that are in different languages has been growing in popularity. Globify is an app that introduces users to top 50 songs from the world!

## System Diagram
![system_diagram](/images/system_diagram.png)

## Data Models
![data_models](/images/data_models.png)

## Features:
1) Users can click countries on an interactive map and redirect to a playlist page containing the top 50 songs for that country
2) Users can search for songs using Spotify API
3) Music player page that play music using Spotify playback SDK. Users can drag or click on the progress bar to change the progress of the song
4) User authentication is implemented using Spotify's Oauth. Users can log out by resetting their auth token

## User Authentication
1) Redirect User to Spotify 
2) User sign in using spotify and redirect to our server with a code
3) Using the user code, Spotify client_id, and Spotify client_secret we fetch an access token for the user. We create a auth token for the user and save it to their session. The access token and auth token are saved for the user in the database.
4) all subsequent requests to our server will be checked to see if the auth_token matches the one in the database. If the auth token match the server will make request to fetch data from Spotify API using the user's access token.

## Pages

### login page & homepage
![data_models](/images/login.gif)

### Interactive map & top 50 country playlist
![data_models](/images/top50.gif)

### Music player 
![data_models](/images/musicplayer.gif)

### Search 
![data_models](/images/search.gif)

## Technologies
* Python
* Flask
* PostgreSQL
* SQLAlchemy
* HTML
* Jinja
* CSS
* JavaScript
* jQuery
* AJAX
* Jvectormap
* Spotify Web API
* Spotify Web Playback SDK



