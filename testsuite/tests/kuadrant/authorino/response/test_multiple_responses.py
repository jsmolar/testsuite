"""Tests multiple responses specified"""
import json

import pytest

from testsuite.objects import Value


@pytest.fixture(scope="module")
def authorization(authorization):
    """Add response to Authorization"""
    authorization.responses.add_json("header", {"anything": Value("one")})
    authorization.responses.add_json("X-Test", {"anything": Value("two")})
    return authorization


def test_multiple_responses(auth, client):
    """Test that both headers are present"""
    response = client.get("/get", auth=auth)

    assert response.status_code == 200
    data = response.json()["headers"].get("Header", None)
    assert data is not None, "Headers from first response (Header) is missing"

    extra_data = json.loads(data)
    assert extra_data["anything"] == "one"

    data = response.json()["headers"].get("X-Test", None)
    assert data is not None, "Headers from second response (X-Test) is missing"

    extra_data = json.loads(data)
    assert extra_data["anything"] == "two"
