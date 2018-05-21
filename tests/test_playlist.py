def test_get_existing_playlist_responds_with_it(client, db, playlist, song, admin_headers):
    playlist.songs.append(song)
    db.session.add(playlist)
    db.session.commit()

    rep = client.get('/api/v1/playlists/%d' % playlist.id, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()['playlist']

    assert data['name'] == playlist.name
    assert len(data['songs']) == 1

    assert data['songs'][0]['name'] == song.name


def test_get_unexisting_playlist_responds_with_404(client, db, playlist, admin_headers):
    # test 404
    rep = client.get("/api/v1/playlists/100000", headers=admin_headers)
    assert rep.status_code == 404


def test_get_all_playlists(client, db, playlist_factory, admin_headers):
    playlists = playlist_factory.create_batch(30)

    db.session.add_all(playlists)
    db.session.commit()

    rep = client.get('/api/v1/playlists', headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()

    assert len(results['results']) == len(playlists)

    for playlist in playlists:
        assert any(u['id'] == playlist.id for u in results['results'])
