import pytest

from refextract.app import create_app


@pytest.fixture(autouse=True, scope="session")
def app():
    app = create_app()
    yield app


@pytest.fixture()
def app_client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_query_parameters": ["access_token"],
        "ignore_localhost": True,
        "decode_compressed_response": True,
        "filter_headers": ("Authorization", "User-Agent"),
        "record_mode": "once",
    }
