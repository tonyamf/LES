from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AdvSearchTest(FunctionalTest):

    def test_can_test(self):
        self.browser.get(self.live_server_url)
