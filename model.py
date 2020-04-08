from flask_sqlalchemy import SQLAlchemy
from secrets import token_urlsafe

# Created an instance of SQLAlchemy class, which represents the connection to the 
# database
db = SQLAlchemy()


class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    spotify_id = db.Column(db.String, primary_key=True)
    display_name = db.Column(db.String(100), nullable=False, default='user')
    access_token = db.Column(db.String(200), nullable=False)
    auth_token = db.Column(db.String(200), nullable=False)


    def __repr__(self):
        """Return a human-readable representation of a User."""
        return f"<User class - display_name:{self.display_name} and spotify_id:{self.spotify_id}>"

    def set_new_auth_token(self):
        self.auth_token = token_urlsafe()
        return self.auth_token

    # format the access token into the header (for request to SPOTIFY API)
    def get_auth_header(self):
        return {
            'Authorization': f'Bearer {self.access_token}'
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class CountryPlaylist(db.Model):
    """Data model for a country_playlist."""

    __tablename__ = "country_playlists"

    country_code = db.Column(db.String(50), primary_key=True)
    playlist_id = db.Column(db.String, nullable=False)
    

    def __repr__(self):
        """Return a human-readable representation of a CountryPlaylist."""
        return f"<CountryPlaylist class - {self.country_code}>"

def connect_to_db(app):

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///music"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # From server.py import app
    from server import app
    connect_to_db(app)
