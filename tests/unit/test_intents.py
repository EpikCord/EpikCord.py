from EpikCord import Intents


def test_intents():
    intents = Intents(guilds=True, members=True)
    assert intents.guilds
    assert intents.members

    assert intents.turned_on == ["guilds", "members"]
    intents.guilds = False

    assert intents.turned_on == ["members"]

    intents.bans = True
    assert intents.turned_on == ["members", "bans"]


def test_intents_none():
    intents = Intents()
    assert intents.turned_on == []


def test_intents_all():
    intents = Intents.all()

    for item in Intents.class_flags:
        assert getattr(intents, item)

    members = list(Intents.class_flags)
    assert intents.turned_on == members
    intents.guilds = False

    assert intents.turned_on == members[1:]
    assert not intents.guilds
