import pytest

from testsuite.kuadrant.policy.rate_limit import RateLimitPolicy, Limit
from testsuite.page_objects.policies.rate_limit_policy import RateLimitNewPage


@pytest.fixture
def rate_limit_policy(navigator, request, cluster, blame, gateway):
    policy = RateLimitPolicy.create_instance(cluster, blame("2rp10m"), gateway)
    policy.add_limit("3rp10s", [Limit(3, 10)])

    new_page = navigator.navigate(RateLimitNewPage)
    new_page.create(policy)
    request.addfinalizer(policy.delete)


def test_a(rate_limit_policy):
    print("a")
