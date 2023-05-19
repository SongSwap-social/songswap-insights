from app import db
from app.models.history import History


def get_top_tracks(user_id):
    result = (
        db.session.query(History.track_id, db.func.count(History.track_id))
        .filter(History.user_id == user_id)
        .group_by(History.track_id)
        .order_by(db.func.count(History.track_id).desc())
        .limit(10)
        .all()
    )

    top_tracks = [{"track_id": r[0], "count": r[1]} for r in result]
    return top_tracks
