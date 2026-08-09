from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://opensource-demo.orangehrmlive.com"
    USERNAME = (By.ID, "txtUsername")
    PASSWORD = (By.ID, "txtPassword")
    LOGIN_BTN = (By.ID, "btnLogin")
    FORGOT_LINK = (By.LINK_TEXT, "Forgot your password?")
    ERROR_MSG = (By.ID, "spanMessage")

    def load(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.send_keys(self.USERNAME, username)
        self.send_keys(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def click_forgot(self):
        self.click(self.FORGOT_LINK)

    def get_error(self):
        el = self.is_visible(self.ERROR_MSG)
        return el.text if el else ""
