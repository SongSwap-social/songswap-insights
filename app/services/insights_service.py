from typing import List

from app import db
from app.models.history import Artists, ArtistTracks, History, Tracks


def get_total_tracks(user_id: int) -> int:
    return db.session.query(History).filter(History.user_id == user_id).count()


def def_distinct_tracks(user_id: int) -> int:
    return (
        db.session.query(History)
        .filter(History.user_id == user_id)
        .group_by(History.track_id)
        .count()
    )


def get_top_tracks(user_id: int, limit: int = 10) -> List[dict]:
    result = (
        db.session.query(
            History.track_id, Tracks.name, Artists.name, db.func.count(History.track_id)
        )
        .join(Tracks, Tracks.id == History.track_id)
        .join(ArtistTracks, ArtistTracks.track_id == Tracks.id)
        .join(Artists, Artists.id == ArtistTracks.artist_id)
        .filter(History.user_id == user_id)
        .filter(ArtistTracks.is_primary == True)
        .group_by(History.track_id, Tracks.name, Artists.name)
        .order_by(db.func.count(History.track_id).desc())
        .limit(limit)
        .all()
    )

    top_tracks = [
        {"track_id": r[0], "track_name": r[1], "artist_name": r[2], "count": r[3]}
        for r in result
    ]
    return top_tracks


def get_top_artists(user_id: int) -> List[dict]:
    result = (
        db.session.query(Artists.id, Artists.name, db.func.count(History.track_id))
        .join(ArtistTracks, ArtistTracks.artist_id == Artists.id)
        .join(Tracks, Tracks.id == ArtistTracks.track_id)
        .join(History, History.track_id == Tracks.id)
        .filter(History.user_id == user_id)
        .group_by(Artists.id, Artists.name)
        .order_by(db.func.count(History.track_id).desc())
        .limit(10)
        .all()
    )

    top_artists = [
        {"artist_id": r[0], "artist_name": r[1], "count": r[2]} for r in result
    ]
    return top_artists


def get_top_primary_artists(user_id: int) -> List[dict]:
    result = (
        db.session.query(Artists.id, Artists.name, db.func.count(History.track_id))
        .join(ArtistTracks, ArtistTracks.artist_id == Artists.id)
        .join(Tracks, Tracks.id == ArtistTracks.track_id)
        .join(History, History.track_id == Tracks.id)
        .filter(History.user_id == user_id)
        .filter(ArtistTracks.is_primary == True)
        .group_by(Artists.id, Artists.name)
        .order_by(db.func.count(History.track_id).desc())
        .limit(10)
        .all()
    )

    top_artists = [
        {"artist_id": r[0], "artist_name": r[1], "count": r[2]} for r in result
    ]
    return top_artists
