from playwright.sync_api import Page

from testsuite.page_objects.navigator import Navigable


class TopologyPage(Navigable):
    def __init__(self, page: Page):
        super().__init__(page)
        self.topology_view = self.page.locator("//div[@class='pf-topology-content']")

    def find_node(self, name):
        node = self.topology_view.locator(f"//*[text() = '{name}']/ancestor::*[@data-type='node']")
        return node.get_attribute("data-id")

    def find_edge(self, node1, node2):
        edge = self.topology_view.locator(f"//*[@data-id='edge-{node1}-{node2}' and @data-kind='edge']")
        return

    def is_displayed(self):
        return self.topology_view
