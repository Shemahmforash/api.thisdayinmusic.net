from thisdayinmusic.extensions import db


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    spotify_id = db.Column(db.String(255), nullable=False)

    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))

    def __init__(self, **kwargs):
        super(Song, self).__init__(**kwargs)

    def __repr__(self):
        return "<Song {} - {} - {}>".format(self.name, self.spotify_id, self.artist)
