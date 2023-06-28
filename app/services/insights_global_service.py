from app import db
from app.models.history import Artists, ArtistTracks, History, Tracks


def get_top_tracks(limit: int = 10) -> dict:
    result = (
        db.session.query(Tracks.name, Artists.name, db.func.count(History.track_id))
        .join(Tracks, Tracks.id == History.track_id)
        .join(ArtistTracks, ArtistTracks.track_id == Tracks.id)
        .join(Artists, Artists.id == ArtistTracks.artist_id)
        .filter(ArtistTracks.is_primary == True)
        .group_by(History.track_id, Tracks.name, Artists.name)
        .order_by(db.func.count(History.track_id).desc())
        .limit(limit)
    )

    return [
        {
            "track_name": track_name,
            "artist_name": artist_name,
            "count": count,
        }
        for track_name, artist_name, count in result
    ]


def get_top_artists(limit: int = 10) -> dict:
    result = (
        db.session.query(Artists.name, db.func.count(History.track_id))
        .join(ArtistTracks, ArtistTracks.artist_id == Artists.id)
        .join(Tracks, Tracks.id == ArtistTracks.track_id)
        .join(History, History.track_id == Tracks.id)
        .filter(ArtistTracks.is_primary == True)
        .group_by(Artists.name)
        .order_by(db.func.count(History.track_id).desc())
        .limit(limit)
    )

    return [
        {"artist_name": artist_name, "count": count} for artist_name, count in result
    ]


def get_top_primary_artists(limit: int = 10) -> dict:
    result = (
        db.session.query(Artists.name, db.func.count(ArtistTracks.track_id))
        .join(ArtistTracks, ArtistTracks.artist_id == Artists.id)
        .filter(ArtistTracks.is_primary == True)
        .group_by(Artists.name)
        .order_by(db.func.count(ArtistTracks.track_id).desc())
        .limit(limit)
    )

    return [
        {"artist_name": artist_name, "count": count} for artist_name, count in result
    ]


def get_top_listeners(limit: int = 10) -> dict:
    result = (
        db.session.query(History.user_id, db.func.count(History.user_id))
        .group_by(History.user_id)
        .order_by(db.func.count(History.user_id).desc())
        .limit(limit)
    )

    return [{"user_id": user_id, "count": count} for user_id, count in result]


def get_total_listens() -> int:
    return db.session.query(History).count()


def get_distinct_tracks() -> int:
    return db.session.query(Tracks).group_by(Tracks.id).count()


def get_distinct_artists() -> int:
    return db.session.query(Artists).group_by(Artists.id).count()


def get_distinct_primary_artists() -> int:
    return (
        db.session.query(Artists)
        .join(ArtistTracks, ArtistTracks.artist_id == Artists.id)
        .filter(ArtistTracks.is_primary == True)
        .group_by(Artists.id)
        .count()
    )


def get_total_listen_time() -> int:
    return (
        db.session.query(History)
        .join(Tracks, Tracks.id == History.track_id)
        .with_entities(db.func.sum(Tracks.duration_ms))
        .scalar()
    )
