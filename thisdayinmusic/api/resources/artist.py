from flask_jwt_extended import jwt_required
from flask_marshmallow import fields
from flask_restful import Resource

from thisdayinmusic.commons.pagination import paginate
from thisdayinmusic.extensions import ma, db
from thisdayinmusic.models.artist import Artist


class ArtistSchema(ma.ModelSchema):
    name = fields.fields.Str()
    spotify_id = fields.fields.Str()

    songs = ma.Nested('SongSchema', many=True, exclude=('artist', 'events'))
    events = ma.Nested('EventSchema', many=True, exclude=('artist', 'song'))

    class Meta:
        model = Artist
        sqla_session = db.session


class ArtistResource(Resource):
    method_decorators = [jwt_required]

    def get(self, artist_id):
        schema = ArtistSchema()
        artist = Artist.query.get_or_404(artist_id)
        return {"artist": schema.dump(artist).data}


class ArtistList(Resource):
    method_decorators = [jwt_required]

    def get(self):
        schema = ArtistSchema(many=True)
        query = Artist.query
        return paginate(query, schema)
