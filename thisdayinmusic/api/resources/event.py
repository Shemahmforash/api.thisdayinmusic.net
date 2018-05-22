from flask_jwt_extended import jwt_required
from flask_marshmallow import fields
from flask_restful import Resource, reqparse
from sqlalchemy import extract

from thisdayinmusic.commons.pagination import paginate
from thisdayinmusic.extensions import ma, db
from thisdayinmusic.models.event import Event


class EventSchema(ma.ModelSchema):
    description = fields.fields.Str()
    date = fields.fields.Date()
    type = fields.fields.Str()

    song = ma.Nested('SongSchema', exclude=('events',))
    artist = ma.Nested('ArtistSchema', exclude=('events',))

    class Meta:
        model = Event
        sqla_session = db.session


class EventResource(Resource):
    method_decorators = [jwt_required]

    def get(self, event_id):
        schema = EventSchema()
        event = Event.query.get_or_404(event_id)
        return {"event": schema.dump(event).data}


class EventList(Resource):
    method_decorators = [jwt_required]

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('month', type=int, help='Month cannot be converted')
        parser.add_argument('day', type=int, help='Day cannot be converted')
        args = parser.parse_args()

        schema = EventSchema(many=True)

        query = self._get_query(args['month'], args['day'])

        return paginate(query, schema)

    def _get_query(self, month=None, day=None):
        query = Event.query

        if day and month:
            query = query.filter(extract('month', Event.date) == month, extract('day', Event.date) == day)

        return query
