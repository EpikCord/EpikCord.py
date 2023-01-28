from EpikCord.utils.loose import clean_url


def test_clean_url():
    url = "channels/1234567890/messages/1234567890"
    assert clean_url(url, 9) == (
        'https://discord.com/api/v9/channels/'
        '1234567890/messages/1234567890'
    )


def test_clean_url_with_slash():
    url = "/channels/1234567890/messages/1234567890"
    assert clean_url(url, 9) == (
        'https://discord.com/api/v9/channels/'
        '1234567890/messages/1234567890'
    )


def test_clean_url_with_version():
    url = "channels/1234567890/messages/1234567890"
    assert clean_url(url, 8) == (
        'https://discord.com/api/v8/channels/'
        '1234567890/messages/1234567890'
    )


def test_clean_url_with_double_slash():
    url = "/channels/1234567890/messages/1234567890/"
    assert clean_url(url, 9) == (
        'https://discord.com/api/v9/channels/'
        '1234567890/messages/1234567890'
    )
