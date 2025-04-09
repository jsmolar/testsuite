import pytest

from testsuite.httpx.auth import HttpxOidcClientAuth
from testsuite.kuadrant.policy.authorization.auth_policy import AuthPolicy
from testsuite.page_objects.policies.auth_policy import AuthNewPage


@pytest.fixture(scope="module")
def auth(oidc_provider):
    """Returns Authentication object for HTTPX"""
    return HttpxOidcClientAuth(oidc_provider.get_token, "authorization")


@pytest.fixture(scope="module")
def auth_policy_instance(cluster, blame, gateway, oidc_provider, label) -> AuthPolicy:
    policy = AuthPolicy.create_instance(cluster, blame("authz"), gateway, labels={"testRun": label})
    policy.identity.add_oidc("default", oidc_provider.well_known["issuer"])
    return policy


@pytest.fixture(autouse=True)
def auth_policy(navigator, request, auth_policy_instance):
    new_page = navigator.navigate(AuthNewPage)
    request.addfinalizer(auth_policy_instance.delete)
    new_page.create(auth_policy_instance)
    auth_policy_instance.wait_for_ready()


def test_a(client, auth):
    response = client.get("/get", auth=auth)
    assert response.status_code == 200
    print("a")
