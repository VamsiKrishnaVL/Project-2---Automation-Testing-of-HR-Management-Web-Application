from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class MyInfoPage(BasePage):
    PERSONAL = (By.LINK_TEXT, "Personal Details")
    CONTACT = (By.LINK_TEXT, "Contact Details")
    EMERGENCY = (By.LINK_TEXT, "Emergency Contacts")
    DEPENDENTS = (By.LINK_TEXT, "Dependents")

    def open_personal(self):
        self.click(self.PERSONAL)

    def open_contact(self):
        self.click(self.CONTACT)

    def open_emergency(self):
        self.click(self.EMERGENCY)

    def open_dependents(self):
        self.click(self.DEPENDENTS)
