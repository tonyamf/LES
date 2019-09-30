from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SentenceTest(FunctionalTest):

    def test_can_create_sentence(self):
        self.browser.get(self.live_server_url)

        self.login()
        nova_frase_input = self.browser.find_element_by_tag_name('a')
        nova_frase_input.send_keys(Keys.ENTER)
