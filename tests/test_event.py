import datetime

import factory
from factory import fuzzy
from pytest_factoryboy import register

from thisdayinmusic.models.event import Event


@register
class EventFactory(factory.Factory):
    description = factory.Sequence(lambda n: 'some event %d' % n)
    date = fuzzy.FuzzyDate(datetime.date(2008, 1, 1))
    type = 'event'

    artist_id = factory.Sequence(lambda n: n)
    song_id = factory.Sequence(lambda n: n)

    class Meta:
        model = Event


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
    for event in events:
        assert any(u['id'] == event.id for u in results['results'])
