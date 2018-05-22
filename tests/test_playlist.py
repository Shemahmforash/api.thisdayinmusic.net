import datetime

import faker


def test_get_existing_playlist_responds_with_it(client, db, playlist, song, admin_headers):
    playlist.songs.append(song)
    db.session.add(playlist)
    db.session.commit()

    rep = client.get('/api/v1/playlists/%d' % playlist.id, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()['playlist']

    assert data['name'] == playlist.name
    assert len(data['songs']) == 1

    assert data['songs'][0] == {
        'id': song.id,
        'name': song.name,
        'spotify_id': song.spotify_id,
        'artist': {
            'id': song.artist.id,
            'name': song.artist.name,
            'spotify_id': song.artist.spotify_id
        },
        'events': []
    }


def test_get_unexisting_playlist_responds_with_404(client, db, playlist, admin_headers):
    # test 404
    rep = client.get("/api/v1/playlists/100000", headers=admin_headers)
    assert rep.status_code == 404


def test_get_all_playlists(client, db, playlist_factory, admin_headers_without_content_type):
    playlists = playlist_factory.create_batch(30)

    db.session.add_all(playlists)
    db.session.commit()

    rep = client.get('/api/v1/playlists', headers=admin_headers_without_content_type)
    assert rep.status_code == 200

    results = rep.get_json()

    assert results['total'] == len(playlists)

    for playlist in playlists:
        assert any(u['id'] == playlist.id for u in results['results'])


def test_filter_playlists_by_date(client, db, playlist_factory, admin_headers_without_content_type):
    fake = faker.Faker()
    some_date = fake.date_object()

    playlists = [
        playlist_factory.create(date=some_date),
        playlist_factory.create(date=some_date - datetime.timedelta(days=1)),
        playlist_factory.create(date=some_date),
        playlist_factory.create(date=some_date + datetime.timedelta(days=1)),
    ]

    db.session.add_all(playlists)
    db.session.commit()

    url = '/api/v1/playlists?month={}&day={}'.format(some_date.month, some_date.day)

    rep = client.get(url, headers=admin_headers_without_content_type)
    assert rep.status_code == 200

    results = rep.get_json()

    assert results['total'] == 2

    for playlist in results['results']:
        assert playlist['date'] == some_date.strftime('%Y-%m-%d')
