import datetime
import json

import factory
import pytest
from factory import fuzzy
from pytest_factoryboy import register

from thisdayinmusic.app import create_app
from thisdayinmusic.extensions import db as _db
from thisdayinmusic.models import User
from thisdayinmusic.models.artist import Artist
from thisdayinmusic.models.event import Event
from thisdayinmusic.models.playlist import Playlist
from thisdayinmusic.models.song import Song


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        username='admin',
        email='admin@admin.com',
        password='admin'
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def artist(db):
    created_artist = Artist(name='some name', spotify_id='some spotify id')

    db.session.add(created_artist)
    db.session.commit()

    return created_artist


@pytest.fixture
def song(artist, db):
    created_song = Song(name='some_name', spotify_id='spotify:some_id', artist=artist)
    db.session.add(created_song)
    db.session.commit()

    return created_song


@pytest.fixture
def event(song, db):
    created_event = Event(description='some random description', date=datetime.date.today(), type='Birth',
                          artist=song.artist, song=song)

    db.session.add(created_event)
    db.session.commit()

    return created_event


@pytest.fixture
def playlist(song, db):
    created_playlist = PlaylistFactory.build(name='some name', date=datetime.date.today(), songs=[song])

    db.session.add(created_playlist)
    db.session.commit()

    return created_playlist


@pytest.fixture
def admin_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@register
class ArtistFactory(factory.Factory):
    name = factory.Faker('name')
    spotify_id = factory.Sequence(lambda n: 'spotify:%d' % n)

    class Meta:
        model = Artist


@register
class SongFactory(factory.Factory):
    name = factory.Faker('name')
    spotify_id = factory.Sequence(lambda n: 'spotify:%d' % n)

    artist = factory.SubFactory(ArtistFactory)

    class Meta:
        model = Song


@register
class EventFactory(factory.Factory):
    description = factory.Faker('text')
    date = fuzzy.FuzzyDate(datetime.date(2008, 1, 1))
    type = 'event'

    artist = factory.SubFactory(ArtistFactory)
    song = factory.SubFactory(SongFactory)

    class Meta:
        model = Event


@register
class PlaylistFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'some playlist %d' % n)
    date = fuzzy.FuzzyDate(datetime.date(2008, 1, 1))

    class Meta:
        model = Playlist


@register
class UserFactory(factory.Factory):
    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@mail.com' % n)
    password = "mypwd"

    class Meta:
        model = User
