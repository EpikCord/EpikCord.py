import pytest

from EpikCord.utils.enums import HTTPCodes, JSONErrorCodes


def test_http_code_5xx():
    assert HTTPCodes(500) == HTTPCodes.SERVER_ERROR
    assert HTTPCodes(502) == HTTPCodes.GATEWAY_UNAVAILABLE

    for _ in range(503, 600):
        assert HTTPCodes(_) == HTTPCodes.SERVER_ERROR


def test_missing_code():
    with pytest.raises(ValueError):
        HTTPCodes(499)

    with pytest.raises(ValueError):
        HTTPCodes(600)


def test_invalid_code():
    with pytest.raises(ValueError):
        HTTPCodes("500")


def test_json_general_error():
    assert JSONErrorCodes(0) == JSONErrorCodes.GENERAL_ERROR
    assert JSONErrorCodes(4815162342) == JSONErrorCodes.GENERAL_ERROR
