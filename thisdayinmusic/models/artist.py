from thisdayinmusic.extensions import db
from thisdayinmusic.models.song import Song


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    spotify_id = db.Column(db.String(255), nullable=False)

    songs = db.relationship(Song, backref="artist")

    def __init__(self, **kwargs):
        super(Artist, self).__init__(**kwargs)

    def __repr__(self):
        return "<Artist {} - {}>".format(self.name, self.spotify_id)
