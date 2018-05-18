import factory
from pytest_factoryboy import register

from thisdayinmusic.models.song import Song


@register
class SongFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'song%d' % n)
    spotify_id = factory.Sequence(lambda n: 'spotify:%d' % n)
    artist_id = factory.Sequence(lambda n: n)

    class Meta:
        model = Song


def test_get_unexisting_song_responds_with_404(client, db, song, admin_headers):
    # test 404
    rep = client.get("/api/v1/songs/100000", headers=admin_headers)
    assert rep.status_code == 404


def test_get_existing_song_responds_with_it(client, db, song, admin_headers):
    db.session.add(song)
    db.session.commit()

    # test get_user
    rep = client.get('/api/v1/songs/%d' % song.id, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()['song']

    assert data['name'] == song.name
    assert data['spotify_id'] == song.spotify_id
    assert data['artist_id'] == song.artist_id


def test_get_all_songs(client, db, song_factory, admin_headers):
    songs = song_factory.create_batch(30)

    db.session.add_all(songs)
    db.session.commit()

    rep = client.get('/api/v1/songs', headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for song in songs:
        assert any(u['id'] == song.id for u in results['results'])
