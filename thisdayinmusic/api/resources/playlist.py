from flask_jwt_extended import jwt_required
from flask_marshmallow import fields
from flask_restful import Resource

from thisdayinmusic.commons.pagination import paginate
from thisdayinmusic.extensions import ma, db
from thisdayinmusic.models.playlist import Playlist


class PlaylistSchema(ma.ModelSchema):
    name = fields.fields.Str()
    date = fields.fields.Date()

    songs = ma.Nested('SongSchema', many=True)

    class Meta:
        model = Playlist
        sqla_session = db.session


class PlaylistResource(Resource):
    method_decorators = [jwt_required]

    def get(self, playlist_id):
        schema = PlaylistSchema()
        playlist = Playlist.query.get_or_404(playlist_id)
        return {"playlist": schema.dump(playlist).data}


class PlaylistList(Resource):
    method_decorators = [jwt_required]

    def get(self):
        schema = PlaylistSchema(many=True)
        query = Playlist.query
        return paginate(query, schema)
