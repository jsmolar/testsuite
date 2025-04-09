import pytest

from testsuite.kuadrant.policy.tls import TLSPolicy
from testsuite.page_objects.policies.tls_policy import TLSNewPage


@pytest.fixture(scope="module")
def tls_policy_instance(blame, gateway, module_label, cluster_issuer):
    """TLSPolicy fixture"""
    policy = TLSPolicy.create_instance(
        gateway.cluster,
        blame("tls"),
        parent=gateway,
        issuer=cluster_issuer,
        labels={"app": module_label},
    )
    return policy


@pytest.fixture(autouse=True)
def tls_policy(tls_policy_instance, navigator, request):
    new_page = navigator.navigate(TLSNewPage)
    request.addfinalizer(tls_policy_instance.delete)
    new_page.create(tls_policy_instance)
    tls_policy_instance.wait_for_ready()


def test_a(tls_policy):
    print("a")
