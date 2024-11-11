from playwright.sync_api import Page

from testsuite.kuadrant.policy.authorization.auth_policy import AuthPolicy
from testsuite.page_objects.navigator import Navigable, step


class AuthNewPage(Navigable):
    def __init__(self, page):
        super().__init__(page)
        self.text_area = page.locator("//textarea[@class='inputarea']")
        self.create_btn = self.page.locator("//button[@id='save-changes']")

    def create(self, auth_policy: AuthPolicy):
        self.text_area.press("Control+a")
        self.text_area.press("Delete")
        self.text_area.fill(str(auth_policy.as_dict()))
        self.create_btn.click()

    def is_displayed(self):
        return self.text_area, self.create_btn


class AuthListPage(Navigable):
    def __init__(self, page: Page):
        super().__init__(page)
        self.new_btn = page.get_by_text("Create AuthPolicy")

    @step(AuthNewPage)
    def new(self):
        self.new_btn.click()

    def is_displayed(self):
        return self.new_btn
