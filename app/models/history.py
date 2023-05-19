from app import db


class History(db.Model):
    __tablename__ = "history"
    date = db.Column(db.Date, primary_key=True)
    time = db.Column(db.Time, primary_key=True)
    track_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, primary_key=True)
