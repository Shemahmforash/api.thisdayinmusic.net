def test_get_existing_event_responds_with_it(client, db, event, admin_headers):
    db.session.add(event)
    db.session.commit()

    # test get_user
    rep = client.get('/api/v1/events/%d' % event.id, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()['event']

    assert data['description'] == event.description
    assert data['date'] == event.date.strftime("%Y-%m-%d")
    assert data['type'] == event.type
    assert data['song']['name'] == event.song.name
    assert data['song']['artist']['name'] == event.artist.name
    assert data['song']['artist']['name'] == event.song.artist.name


def test_get_unexisting_event_responds_with_404(client, db, event, admin_headers):
    # test 404
    rep = client.get("/api/v1/events/100000", headers=admin_headers)
    assert rep.status_code == 404


def test_get_all_events(client, db, event_factory, admin_headers):
    events = event_factory.create_batch(30)

    db.session.add_all(events)
    db.session.commit()

    rep = client.get('/api/v1/events', headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()

    assert len(results['results']) == len(events)

    for event in events:
        assert any(u['id'] == event.id for u in results['results'])
