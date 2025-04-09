from testsuite.kuadrant.policy.rate_limit import RateLimitPolicy
from testsuite.page_objects.navigator import Navigable, step


class RateLimitNewPage(Navigable):

    def __init__(self, page):
        super().__init__(page)
        self.text_area = page.locator("//textarea[@class='inputarea']")
        self.create_btn = self.page.locator("//button[@id='save-changes']")

    def create(self, rlp: RateLimitPolicy):
        self.text_area.press("Control+a")
        self.text_area.press("Delete")
        self.text_area.fill(str(rlp.as_dict()))
        self.create_btn.click()

    def is_displayed(self):
        return self.text_area, self.create_btn


class RateLimitListPage(Navigable):
    def __init__(self, page):
        super().__init__(page)
        self.new_btn = page.get_by_text("Create RateLimitPolicy")

    @step(RateLimitNewPage)
    def new(self):
        self.new_btn.click()

    def is_displayed(self):
        return self.new_btn
