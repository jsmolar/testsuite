"""Test for API key auth credentials"""
import pytest

from testsuite.objects import Credentials


@pytest.fixture(scope="module", params=["authorizationHeader", "customHeader", "queryString", "cookie"])
def credentials(request):
    """Location where are auth credentials passed"""
    return Credentials(request.param, "APIKEY")


@pytest.fixture(scope="module")
def authorization(authorization, api_key, credentials):
    """Add API key identity to AuthConfig"""
    authorization.identity.clear_all()
    authorization.identity.add_api_key("api_key", credentials=credentials, selector=api_key.selector)
    return authorization


def test_custom_selector(client, auth, credentials):
    """Test if auth credentials are stored in right place"""
    response = client.get("/get", headers={"authorization": "API_KEY " + auth.api_key})
    if credentials == "authorizationHeader":
        assert response.status_code == 200
    else:
        assert response.status_code == 401


def test_custom_header(client, auth, credentials):
    """Test if auth credentials are stored in right place"""
    response = client.get("/get", headers={"API_KEY": auth.api_key})
    if credentials == "customHeader":
        assert response.status_code == 200
    else:
        assert response.status_code == 401


def test_query(client, auth, credentials):
    """Test if auth credentials are stored in right place"""
    response = client.get("/get", params={"API_KEY": auth.api_key})
    if credentials == "queryString":
        assert response.status_code == 200
    else:
        assert response.status_code == 401


def test_cookie(route, auth, credentials):
    """Test if auth credentials are stored in right place"""
    with route.client(cookies={"API_KEY": auth.api_key}) as client:
        response = client.get("/get")
        if credentials == "cookie":
            assert response.status_code == 200
        else:
            assert response.status_code == 401
