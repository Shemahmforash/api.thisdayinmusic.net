from flask import Blueprint
from flask_restful import Api

from thisdayinmusic.api.resources import UserResource, UserList
from thisdayinmusic.api.resources.artist import ArtistResource, ArtistList
from thisdayinmusic.api.resources.event import EventResource, EventList
from thisdayinmusic.api.resources.playlist import PlaylistResource, PlaylistList
from thisdayinmusic.api.resources.song import SongResource, SongList

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(SongResource, '/songs/<int:song_id>')
api.add_resource(SongList, '/songs')

api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')

api.add_resource(ArtistResource, '/artists/<int:artist_id>')
api.add_resource(ArtistList, '/artists')

api.add_resource(EventResource, '/events/<int:event_id>')
api.add_resource(EventList, '/events')

api.add_resource(PlaylistResource, '/playlists/<int:playlist_id>')
api.add_resource(PlaylistList, '/playlists')
