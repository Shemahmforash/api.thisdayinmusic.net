from thisdayinmusic.extensions import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)

    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
