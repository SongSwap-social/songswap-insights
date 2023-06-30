from app import db

CASCADE = {  # Cascade behavior at DB level
    "ondelete": "CASCADE",
    "onupdate": "CASCADE",
}


class History(db.Model):
    __tablename__ = "History"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("Users.id", **CASCADE),
        nullable=False,
        primary_key=True,
    )
    played_at = db.Column(db.DateTime, nullable=False, primary_key=True)
    track_id = db.Column(
        db.String(24), db.ForeignKey("Tracks.id", **CASCADE), nullable=False
    )

    def __repr__(self):
        return f"History('{self.user_id}', '{self.played_at}', '{self.track_id}')"


class Artists(db.Model):
    __tablename__ = "Artists"
    _relationship_options = {  # Cascade behavior at ORM level
        "backref": "artist",
        "lazy": True,
        "cascade": "all, delete-orphan",
    }

    id = db.Column(db.String(24), primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    # Delete the ArtistTracks when an artist is deleted
    tracks = db.relationship("ArtistTracks", **_relationship_options)

    # Delete the ArtistImages when an artist is deleted
    images = db.relationship("ArtistImages", **_relationship_options)

    # Delete the ArtistPopularity when an artist is deleted
    popularity = db.relationship("ArtistPopularity", **_relationship_options)

    # Delete the ArtistGenres when an artist is deleted
    genres = db.relationship("ArtistGenres", **_relationship_options)

    # Delete the ArtistFollowers when an artist is deleted
    followers = db.relationship("ArtistFollowers", **_relationship_options)

    def __repr__(self):
        return f"Artist('{self.name}')"


class Tracks(db.Model):
    __tablename__ = "Tracks"
    _relationship_options = {
        "backref": "track",
        "lazy": True,
        "cascade": "all, delete-orphan",
    }

    id = db.Column(db.String(24), primary_key=True)
    name = db.Column(db.String(240), nullable=False)
    duration_ms = db.Column(db.Integer, nullable=False)

    # Delete the ArtistTracks when a track is deleted
    artists = db.relationship("ArtistTracks", **_relationship_options)

    # Delete the TrackPopularity when a track is deleted
    popularity = db.relationship("TrackPopularity", **_relationship_options)

    # Delete the TrackFeatures when a track is deleted
    features = db.relationship("TrackFeatures", **_relationship_options)

    # Delete the History when a track is deleted
    history = db.relationship("History", **_relationship_options)

    # Delete the TrackImages when a track is deleted
    images = db.relationship("TrackImages", **_relationship_options)

    # Delete the TrackPreviews when a track is deleted
    previews = db.relationship("TrackPreviews", **_relationship_options)

    def __repr__(self):
        return f"Track('{self.name}')"


class ArtistTracks(db.Model):
    __tablename__ = "ArtistTracks"

    track_id = db.Column(
        db.String(24), db.ForeignKey("Tracks.id", **CASCADE), primary_key=True
    )
    artist_id = db.Column(
        db.String(24), db.ForeignKey("Artists.id", **CASCADE), primary_key=True
    )
    is_primary = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return (
            f"ArtistTracks('{self.track_id}', '{self.artist_id}', '{self.is_primary}')"
        )


class TrackPopularity(db.Model):
    __tablename__ = "TrackPopularity"

    id = db.Column(
        db.String(24), db.ForeignKey("Tracks.id", **CASCADE), primary_key=True
    )
    date = db.Column(db.DateTime, nullable=False, primary_key=True)
    popularity = db.Column(db.Integer, nullable=False)


class TrackFeatures(db.Model):
    # https://developer.spotify.com/documentation/web-api/reference/get-audio-features
    __tablename__ = "TrackFeatures"

    id = db.Column(
        db.String(24), db.ForeignKey("Tracks.id", **CASCADE), primary_key=True
    )
    acousticness = db.Column(db.Float, nullable=False)
    danceability = db.Column(db.Float, nullable=False)
    energy = db.Column(db.Float, nullable=False)
    instrumentalness = db.Column(db.Float, nullable=False)
    key = db.Column(db.Integer, nullable=False)
    liveness = db.Column(db.Float, nullable=False)
    loudness = db.Column(db.Float, nullable=False)
    mode = db.Column(db.Integer, nullable=False)
    speechiness = db.Column(db.Float, nullable=False)
    tempo = db.Column(db.Float, nullable=False)
    time_signature = db.Column(db.Integer, nullable=False)
    valence = db.Column(db.Float, nullable=False)


class TrackImages(db.Model):
    __tablename__ = "TrackImages"

    id = db.Column(
        db.String(24), db.ForeignKey("Tracks.id", **CASCADE), primary_key=True
    )
    height = db.Column(db.Integer, nullable=False, primary_key=True)
    width = db.Column(db.Integer, nullable=False, primary_key=True)
    url = db.Column(db.String(240), nullable=False)


class TrackPreviews(db.Model):
    __tablename__ = "TrackPreviews"

    id = db.Column(
        db.String(24), db.ForeignKey("Tracks.id", **CASCADE), primary_key=True
    )
    url = db.Column(db.String(240), nullable=False)


class ArtistImages(db.Model):
    __tablename__ = "ArtistImages"

    id = db.Column(
        db.String(24), db.ForeignKey("Artists.id", **CASCADE), primary_key=True
    )
    height = db.Column(db.Integer, nullable=False, primary_key=True)
    width = db.Column(db.Integer, nullable=False, primary_key=True)
    url = db.Column(db.String(240), nullable=False)


class ArtistPopularity(db.Model):
    __tablename__ = "ArtistPopularity"

    id = db.Column(
        db.String(24), db.ForeignKey("Artists.id", **CASCADE), primary_key=True
    )
    date = db.Column(db.DateTime, nullable=False, primary_key=True)
    popularity = db.Column(db.Integer, nullable=False)


class ArtistGenres(db.Model):
    __tablename__ = "ArtistGenres"

    id = db.Column(
        db.String(24), db.ForeignKey("Artists.id", **CASCADE), primary_key=True
    )
    genre = db.Column(db.String(120), nullable=False, primary_key=True)


class ArtistFollowers(db.Model):
    __tablename__ = "ArtistFollowers"

    id = db.Column(
        db.String(24), db.ForeignKey("Artists.id", **CASCADE), primary_key=True
    )
    date = db.Column(db.DateTime, nullable=False, primary_key=True)
    followers = db.Column(db.Integer, nullable=False)
