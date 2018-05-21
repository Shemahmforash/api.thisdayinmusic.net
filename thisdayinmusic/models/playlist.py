from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from thisdayinmusic.extensions import db

association_table = Table('playlist_song', db.metadata,
                          Column('playlist_id', Integer, ForeignKey('playlist.id')),
                          Column('song_id', Integer, ForeignKey('song.id'))
                          )


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)

    songs = relationship("Song",
                         secondary=association_table)
