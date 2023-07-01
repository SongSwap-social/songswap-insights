from typing import List

from app import db
from app.models.history import (
    Artists,
    ArtistTracks,
    History,
    TrackImages,
    TrackPreviews,
    Tracks,
)

from config import DEBUG


def print_sql(query):
    """
    Helper function to print the SQL query for debugging purposes.

    Args:
        query (SQLAlchemy query): The query to print.
    """
    print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))


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
    # Subquery to get the maximum width image per track
    max_track_images = (
        db.session.query(
            TrackImages.id, db.func.max(TrackImages.width).label("max_width")
        )
        .group_by(TrackImages.id)
        .subquery()
    )

    default_image_url = "https://ia801504.us.archive.org/35/items/mbid-2e999a18-f74d-49f4-8e01-d4f354ad5a32/mbid-2e999a18-f74d-49f4-8e01-d4f354ad5a32-30261100157.jpg"

    result = (
        db.session.query(
            History.track_id,
            Tracks.name,
            Artists.name,
            db.func.count(History.track_id),
            Tracks.duration_ms,
            db.func.coalesce(TrackImages.url, default_image_url).label("image_url"),
            TrackPreviews.url.label("preview_url"),
        )
        .join(Tracks, Tracks.id == History.track_id)
        .join(ArtistTracks, ArtistTracks.track_id == Tracks.id)
        .join(Artists, Artists.id == ArtistTracks.artist_id)
        # Use a LEFT OUTER JOIN to include tracks without images and previews
        .outerjoin(max_track_images, Tracks.id == max_track_images.c.id)
        .outerjoin(
            TrackImages,
            db.and_(
                TrackImages.id == max_track_images.c.id,
                TrackImages.width == max_track_images.c.max_width,
            ),
        )
        .outerjoin(TrackPreviews, TrackPreviews.id == Tracks.id)
        .filter(History.user_id == user_id)
        .filter(ArtistTracks.is_primary == True)
        .group_by(
            History.track_id,
            Tracks.name,
            Artists.name,
            Tracks.duration_ms,
            TrackImages.url,
            TrackPreviews.url,
        )
        .order_by(db.func.count(History.track_id).desc())
        .limit(limit)
    )

    top_tracks = [
        {
            "track_id": r[0],
            "track_name": r[1],
            "artist_name": r[2],
            "count": r[3],
            "duration_ms": r[4],
            "image_url": r[5],
            "preview_url": r[6],
        }
        for r in result
    ]

    if DEBUG:
        print_sql(result)
    return top_tracks


def get_top_artists(user_id: int, limit: int = 10) -> List[dict]:
    result = (
        db.session.query(Artists.id, Artists.name, db.func.count(History.track_id))
        .join(ArtistTracks, ArtistTracks.artist_id == Artists.id)
        .join(Tracks, Tracks.id == ArtistTracks.track_id)
        .join(History, History.track_id == Tracks.id)
        .filter(History.user_id == user_id)
        .group_by(Artists.id, Artists.name)
        .order_by(db.func.count(History.track_id).desc())
        .limit(limit)
    )

    top_artists = [
        {"artist_id": r[0], "artist_name": r[1], "count": r[2]} for r in result
    ]
    return top_artists


def get_top_primary_artists(user_id: int, limit: int = 10) -> List[dict]:
    result = (
        db.session.query(Artists.id, Artists.name, db.func.count(History.track_id))
        .join(ArtistTracks, ArtistTracks.artist_id == Artists.id)
        .join(Tracks, Tracks.id == ArtistTracks.track_id)
        .join(History, History.track_id == Tracks.id)
        .filter(History.user_id == user_id)
        .filter(ArtistTracks.is_primary == True)
        .group_by(Artists.id, Artists.name)
        .order_by(db.func.count(History.track_id).desc())
        .limit(limit)
    )

    top_artists = [
        {"artist_id": r[0], "artist_name": r[1], "count": r[2]} for r in result
    ]
    return top_artists
