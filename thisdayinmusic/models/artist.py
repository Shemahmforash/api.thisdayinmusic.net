from thisdayinmusic.extensions import db


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    spotify_id = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        super(Artist, self).__init__(**kwargs)

    def __repr__(self):
        return "<Artist {} - {}>".format(self.name, self.spotify_id)
