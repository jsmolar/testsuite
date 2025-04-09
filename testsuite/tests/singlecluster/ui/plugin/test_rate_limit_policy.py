import pytest

from testsuite.kuadrant.policy.rate_limit import RateLimitPolicy, Limit
from testsuite.page_objects.policies.rate_limit_policy import RateLimitNewPage


@pytest.fixture(scope="module")
def rlp_instance(cluster, blame, gateway, label):
    policy = RateLimitPolicy.create_instance(cluster, blame("2rp10m"), gateway, labels={"testRun": label})
    policy.add_limit("3rp10s", [Limit(3, "10s")])
    return policy


@pytest.fixture(autouse=True)
def rate_limit_policy(rlp_instance, navigator, request):
    new_page = navigator.navigate(RateLimitNewPage)
    request.addfinalizer(rlp_instance.delete)
    new_page.create(rlp_instance)
    rlp_instance.wait_for_ready()


def test_a(client, rlp_instance):
    rlp_instance.refresh()
    responses = client.get_many("/get", 3)
    responses.assert_all(status_code=200)

    response = client.get("/get")
    assert response.status_code == 429
