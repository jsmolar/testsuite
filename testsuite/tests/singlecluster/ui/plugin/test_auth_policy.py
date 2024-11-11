import pytest

from testsuite.kuadrant.policy.authorization.auth_policy import AuthPolicy
from testsuite.page_objects.policies.auth_policy import AuthNewPage


@pytest.fixture
def auth_policy(navigator, request, cluster, blame, gateway, oidc_provider):
    policy = AuthPolicy.create_instance(cluster, blame("authz"), gateway)
    policy.identity.add_oidc("default", oidc_provider.well_known["issuer"])

    new_page = navigator.navigate(AuthNewPage)
    new_page.create(policy)
    request.addfinalizer(policy.delete)
    return policy


def test_a(auth_policy, client):
    print("a")
