import pytest

from testsuite.page_objects.nav_bar import NavBar
from testsuite.page_objects.navigator import Navigator


@pytest.fixture(autouse=True)
def login(page, base_domain):
    page.goto(f"https://console-openshift-console.{base_domain}")
    page.locator("//a[@title='Log in with htpasswd']").click()
    page.locator("//input[@name='username']").fill("admin")
    page.locator("//input[@name='password']").fill("CHANGEME")
    page.locator("//button[@type='submit']").click()
    return NavBar(page)


@pytest.fixture(autouse=True)
def dynamic_plugin(login, page):
    if not login.kuadrant_nav.is_visible:
        page.locator("//button[@data-test='Dynamic Plugins']").click()
        page.locator("//a[@href='/k8s/cluster/operator.openshift.io~v1~Console/cluster/console-plugins']").click()
        page.locator(
            "//tr[.//a[@data-test-id='kuadrant-console-plugin']]//button[@data-test='edit-console-plugin']"
        ).click()
        page.locator("//input[@value='enabled']").check()


@pytest.fixture
def navigator(page):
    return Navigator(page)
