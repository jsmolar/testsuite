import pytest

from testsuite.kubernetes.monitoring import MetricsEndpoint
from testsuite.kubernetes.monitoring.service_monitor import ServiceMonitor
from testsuite.kubernetes.service import Service, ServicePort


@pytest.fixture(scope="module")
def create_service_monitor(cluster, request, testconfig):
    """Creates Service Monitor"""

    def _create_monitor(name, match_labels, endpoints=None, namespace="global-operators"):
        if endpoints is None:
            endpoints = [MetricsEndpoint("/metrics", "metrics")]

        monitor = ServiceMonitor.create_instance(
            cluster.change_project(namespace),
            name,
            endpoints,
            match_labels=match_labels,
        )
        request.addfinalizer(monitor.delete)
        monitor.commit()
        return monitor

    return _create_monitor


@pytest.fixture(scope="module")
def kuadrant_monitor(blame, create_service_monitor):
    return create_service_monitor(blame("kuadrant-operator-sm"), {"control-plane": "controller-manager"})


@pytest.fixture(scope="module")
def authorino_monitor(blame, create_service_monitor):
    """"""
    return create_service_monitor(blame("authorino-operator-sm"), {"control-plane": "authorino-operator"})


@pytest.fixture(scope="module")
def limitador_monitor(blame, create_service_monitor):
    """"""
    return create_service_monitor(
        blame("limitador-sm"), {"operators.coreos.com/limitador-operator.global-operators": ""}
    )


@pytest.fixture(scope="module")
def dns_monitor(blame, create_service_monitor):
    """"""
    return create_service_monitor(blame("dns-operator-sm"), {"control-plane": "dns-operator-controller-manager"})


@pytest.fixture(scope="module")
def gateway_monitor(cluster, request, gateway, blame, create_service_monitor):
    """"""
    proxy_service = Service.create_instance(
        cluster.change_project("kuadrant"),
        blame("proxy-service"),
        selector={"istio.io/gateway-name": gateway.name()},
        labels={"istio.io/gateway-name": gateway.name()},
        ports=[ServicePort(name="metrics", port=15020, targetPort=15020)],
    )
    request.addfinalizer(proxy_service.delete)
    proxy_service.commit()
    return create_service_monitor(
        blame("gateway-sm"),
        {"istio.io/gateway-name": gateway.name()},
        [MetricsEndpoint("/stats/prometheus", "metrics")],
        namespace="kuadrant",
    )


@pytest.fixture(scope="module", autouse=True)
def wait_for_active_targets(
    prometheus, kuadrant_monitor, authorino_monitor, limitador_monitor, dns_monitor, gateway_monitor
):
    """Waits for all endpoints in Pod Monitor to become active targets"""
    for monitor in [
        kuadrant_monitor,
        authorino_monitor,
        limitador_monitor,
        dns_monitor,
        gateway_monitor,
    ]:
        assert prometheus.is_reconciled(
            monitor
        ), f"Service monitor {monitor.name()} was not reconciled by Prometheus: {monitor.model}"


@pytest.fixture(scope="module")
def route(route, backend):
    route.model.metadata["labels"].update({"service": backend.service.name(), "deployment": backend.deployment.name()})
    route.apply()
    return route
