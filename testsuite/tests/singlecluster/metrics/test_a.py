import pytest


def test_a(client):
    client.get_many("/get", 5)
    print("a")
