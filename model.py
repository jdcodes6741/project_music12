from flask_sqlalchemy import SQLAlchemy

# Created an instance of SQLAlchemy class, which represents the connection to the 
# database
db = SQLAlchemy()


# Created a class called User and inherits from the db.Model (that is how it conencts to the 
# database, M is uppercase so it is a class in SQLAlchemy, used to connect to the database)
class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    # Every table should have a primary_key and should be a unique identifier (In this case, I used 
    # the spotify_id)
    spotify_id = db.Column(db.String, primary_key=True)
    display_name = db.Column(db.String(50), nullable=False, default='user')
    access_key = db.Column(db.String(50), nullable=False)
    auth_key = db.Column(db.String(50), nullable=False)

    # Friendly representation of the object when you print it. Usually prints the class name and 
    # memory address location.
    def __repr__(self):
        """Return a human-readable representation of a User."""
        return f"<User class - display_name:{self.display_name} and spotify_id:{self.spotify_id}>"
    

class CountryPlaylist(db.Model):
    """Data model for a country_playlist."""

    __tablename__ = "country_playlists"

    playlist_id = db.Column(db.String, primary_key=True)
    display_name = db.Column(db.String(50), nullable=False, default='playlist')
    country_code = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Return a human-readable representation of a CountryPlaylist."""
        return f"<CountryPlaylist class - {self.display_name}>"

# Standard function, pass in the application inside server.py
# Can pull information from the database onto our server (you can read and write to the database)
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    # Where to connect to the database
    # Connects the server (app) to the databse
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
