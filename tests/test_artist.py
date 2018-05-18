import factory
from pytest_factoryboy import register

from thisdayinmusic.models.artist import Artist


@register
class ArtistFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'artist%d' % n)
    spotify_id = factory.Sequence(lambda n: 'spotify:%d' % n)

    class Meta:
        model = Artist


def test_get_unexisting_artist_responds_with_404(client, db, artist, admin_headers):
    # test 404
    rep = client.get("/api/v1/artists/100000", headers=admin_headers)
    assert rep.status_code == 404


def test_get_existing_artist_responds_with_it(client, db, artist, admin_headers):
    db.session.add(artist)
    db.session.commit()

    # test get_user
    rep = client.get('/api/v1/artists/%d' % artist.id, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()['artist']

    assert data['name'] == artist.name
    assert data['spotify_id'] == artist.spotify_id


def test_get_all_artists(client, db, artist_factory, admin_headers):
    artists = artist_factory.create_batch(30)

    db.session.add_all(artists)
    db.session.commit()

    rep = client.get('/api/v1/artists', headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for artist in artists:
        assert any(u['id'] == artist.id for u in results['results'])
