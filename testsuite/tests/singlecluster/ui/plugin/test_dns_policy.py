import pytest

from testsuite.kuadrant.policy.dns import LoadBalancing, DNSPolicy
from testsuite.page_objects.policies.dns_policy import DNSNewPage


@pytest.fixture
def dns_policy(navigator, request, cluster, blame, gateway, dns_provider_secret, testconfig):
    load_balancing = LoadBalancing(defaultGeo=True, geo="EU", weight=10)
    policy = DNSPolicy.create_instance(cluster, blame("dns"), gateway, dns_provider_secret, load_balancing)

    new_page = navigator.navigate(DNSNewPage)
    new_page.create(policy)
    request.addfinalizer(policy.delete)


def test_a(dns_policy):
    print("a")
