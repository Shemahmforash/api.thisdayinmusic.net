from thisdayinmusic.models import User, Artist, Song


def user_factory(i):
    return User(
        username="user{}".format(i),
        email="user{}@mail.com".format(i)
    )


def artist_factory(i):
    return Artist(
        name="name{}".format(i),
        spotify_id="spotify:{}".format(i)
    )


def song_factory(i):
    return Song(
        name="name{}".format(i),
        spotify_id="spotify:{}".format(i),
        artist=artist_factory(i)
    )


def event_factory(i):
    return Song(
        description="name{}".format(i),
        song=song_factory(i)
    )
