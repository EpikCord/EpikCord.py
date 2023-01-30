import io

from EpikCord.file import File


def test_file():
    file = File("test.txt", io.BytesIO(b"test"))

    assert file.filename == "test.txt"
    assert file.mime_type == "text/plain"
    assert file.description is None


def test_file_spoiler():
    file = File("test.txt", io.BytesIO(b"test"), spoiler=True)

    assert file.filename == "SPOILER_test.txt"
    assert file.mime_type == "text/plain"
    assert file.description is None