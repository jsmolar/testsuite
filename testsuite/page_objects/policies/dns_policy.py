from playwright.sync_api import Page

from testsuite.gateway import Gateway
from testsuite.kuadrant.policy.dns import LoadBalancing, DNSPolicy
from testsuite.page_objects.navigator import Navigable, step


class DNSNewPage(Navigable):

    def __init__(self, page: Page):
        super().__init__(page)
        self.name_input = self.page.locator("//input[@id='policy-name']")
        self.gateway_select = self.page.locator("//select[@id='gateway-select']")
        self.provider_ref_input = self.page.locator("//input[@id='provider-ref']")
        self.weight_input = self.page.locator("//input[@id='weight']")
        self.geo_input = self.page.locator("//input[@id='geo']")
        self.create_btn = self.page.get_by_text("Create", exact=True)

    def create(self, dns_policy: DNSPolicy):
        self.name_input.fill(dns_policy.model.metadata.name)
        self.gateway_select.select_option(value=f"kuadrant/{dns_policy.model.spec["targetRef"]["name"]}")
        self.provider_ref_input.fill(dns_policy.model.spec["providerRefs"][0]["name"])
        self.weight_input.fill(str(dns_policy.model.spec["loadBalancing"]["weight"]))
        self.geo_input.fill(dns_policy.model.spec["loadBalancing"]["geo"])
        if dns_policy.model.spec["loadBalancing"]["defaultGeo"]:
            self.page.locator("//input[@id='default-geo-enabled']").check()
        else:
            self.page.locator("//input[@id='default-geo-disabled']").check()
        self.create_btn.click()

    def is_displayed(self):
        return self.name_input, self.gateway_select, self.provider_ref_input, self.weight_input


class DNSListPage(Navigable):
    def __init__(self, page: Page):
        super().__init__(page)
        self.new_btn = page.get_by_text("Create DNSPolicy")

    @step(DNSNewPage)
    def new(self):
        self.new_btn.click()

    def is_displayed(self):
        return self.new_btn
