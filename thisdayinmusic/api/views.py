from flask import Blueprint
from flask_restful import Api

from thisdayinmusic.api.resources import UserResource, UserList
from thisdayinmusic.api.resources.artist import ArtistResource, ArtistList

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')

api.add_resource(ArtistResource, '/artists/<int:artist_id>')
api.add_resource(ArtistList, '/artists')
