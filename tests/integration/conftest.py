import pytest


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_query_parameters": ["access_token"],
        "ignore_localhost": True,
        "decode_compressed_response": True,
        "filter_headers": ("Authorization", "User-Agent"),
        "record_mode": "once",
    }
