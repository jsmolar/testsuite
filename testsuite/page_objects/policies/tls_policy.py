from playwright.sync_api import Page

from testsuite.kuadrant.policy.tls import TLSPolicy
from testsuite.page_objects.navigator import Navigable, step


class TLSNewPage(Navigable):
    def __init__(self, page: Page):
        super().__init__(page)
        self.policy_name = self.page.locator("//input[@id='simple-form-policy-name-01']")
        self.gateway_select = self.page.locator("//select[@id='gateway-select']")
        self.cluster_issuer_checkbox = self.page.locator("//input[@id='cluster-issuer']")
        self.issuer_checkbox = self.page.locator("//input[@id='issuer']")
        self.cluster_issuer_select = self.page.locator("//select[@id='clusterissuer-select']")
        self.create_button = self.page.get_by_text("Create", exact=True)

    def create(self, tls_policy: TLSPolicy):
        self.policy_name.fill(tls_policy.model.metadata.name)
        target_ref_name = tls_policy.model.spec.get("targetRef", {}).get("name", "")
        self.gateway_select.select_option(value=f"kuadrant/{target_ref_name}")
        issuer_kind = tls_policy.model.spec.get("issuerRef", {}).get("kind", "")
        if issuer_kind == "ClusterIssuer":
            self.cluster_issuer_checkbox.check()
        else:
            self.issuer_checkbox.check()
        issuer_name = tls_policy.model.spec.get("issuerRef", {}).get("name", "")
        self.cluster_issuer_select.select_option(issuer_name)
        self.create_button.click()

    def is_displayed(self):
        return self.policy_name, self.gateway_select, self.cluster_issuer_select


class TLSListPage(Navigable):
    def __init__(self, page: Page):
        super().__init__(page)
        self.new_btn = page.get_by_text("Create TLSPolicy")

    @step(TLSNewPage)
    def new(self):
        self.new_btn.click()

    def is_displayed(self):
        return self.new_btn
