from EpikCord import Intents


def test_intents():
    intents = Intents(guilds=True, guild_members=True)
    assert intents.GUILDS
    assert intents.GUILD_MEMBERS

    assert intents.turned_on == ["GUILDS", "GUILD_MEMBERS"]
    intents.GUILDS = False

    assert intents.turned_on == ["GUILD_MEMBERS"]

    intents.GUILD_MODERATION = True
    assert intents.turned_on == ["GUILD_MEMBERS", "GUILD_MODERATION"]


def test_intents_none():
    intents = Intents()
    assert intents.turned_on == []


def test_intents_all():
    intents = Intents.all()

    for item in Intents.class_flags:
        assert getattr(intents, item)

    members = list(Intents.class_flags)
    assert intents.turned_on == members
    intents.GUILDS = False

    assert intents.turned_on == members[1:]
    assert not intents.GUILDS


def test_intents_value():
    intents = Intents()

    assert intents.value == 0
    intents.GUILDS = True

    assert intents.value == intents.GUILDS
