from testsuite.page_objects.navigator import step, Navigable
from testsuite.page_objects.policies.policies import PoliciesPage


class NavBar(Navigable):
    def __init__(self, page):
        super().__init__(page)
        self.kuadrant_nav = self.page.locator("//button[@class='pf-v5-c-nav__link' and text() = 'Kuadrant']")

    def expand_kuadrant(self):
        if self.kuadrant_nav.get_attribute("aria-expanded") == "false":
            self.kuadrant_nav.click()

    def overview(self):
        self.expand_kuadrant()

    @step(PoliciesPage)
    def policies(self):
        self.expand_kuadrant()
        self.page.locator("//a[@class='pf-v5-c-nav__link' and text() = 'Policies']").click()

    def topology(self):
        self.expand_kuadrant()

    def is_displayed(self):
        return self.kuadrant_nav
