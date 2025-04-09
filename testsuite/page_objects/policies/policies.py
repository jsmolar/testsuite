from testsuite.page_objects.policies.auth_policy import AuthListPage
from testsuite.page_objects.navigator import step, Navigable
from testsuite.page_objects.policies.dns_policy import DNSListPage
from testsuite.page_objects.policies.rate_limit_policy import RateLimitListPage
from testsuite.page_objects.policies.tls_policy import TLSListPage


class PoliciesPage(Navigable):
    def __init__(self, page):
        super().__init__(page)
        self.dns_tab = self.page.locator("//a[@data-test-id='horizontal-link-DNS']")
        self.tls_tab = self.page.locator("//a[@data-test-id='horizontal-link-TLS']")
        self.auth_tab = self.page.locator("//a[@data-test-id='horizontal-link-Auth']")
        self.rate_limit_tab = self.page.locator("//a[@data-test-id='horizontal-link-RateLimit']")

    def change_project(self, name):
        self.page.locator("//button[@class='pf-v5-c-menu-toggle co-namespace-dropdown__menu-toggle']").click()
        self.page.locator(f"//span[text() = '{name}']").click()

    @step(DNSListPage)
    def dns(self):
        self.change_project("kuadrant")
        self.dns_tab.click()

    @step(TLSListPage)
    def tls(self):
        self.change_project("kuadrant")
        self.tls_tab.click()

    @step(AuthListPage)
    def auth(self):
        self.change_project("kuadrant")
        self.auth_tab.click()

    @step(RateLimitListPage)
    def rate_limit(self):
        self.change_project("kuadrant")
        self.rate_limit_tab.click()

    def is_displayed(self):
        return self.dns_tab, self.tls_tab, self.auth_tab, self.rate_limit_tab
