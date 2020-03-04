from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    spotify_id = db.Column(db.String, primary_key=True)
    display_name = db.Column(db.String(50), nullable=False, default='user')
    access_key = db.Column(db.String(50), nullable=False)
    auth_key = db.Column(db.String(50), nullable=False)

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


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///musical"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
