import pytest

from testsuite.kuadrant.policy.tls import TLSPolicy
from testsuite.page_objects.policies.tls_policy import TLSNewPage


@pytest.fixture
def tls_policy(navigator, request, cluster, blame, gateway, cluster_issuer):
    policy = TLSPolicy.create_instance(cluster, blame("tls"), parent=gateway, issuer=cluster_issuer)

    new_page = navigator.navigate(TLSNewPage)
    new_page.create(policy)
    request.addfinalizer(policy.delete)


def test_a(tls_policy):
    print("a")
