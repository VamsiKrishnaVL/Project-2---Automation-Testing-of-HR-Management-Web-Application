from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class AdminPage(BasePage):
    USER_MANAGEMENT = (By.ID, "menu_admin_UserManagement")
    USERS = (By.ID, "menu_admin_viewSystemUsers")
    ADD_BTN = (By.ID, "btnAdd")
    USER_ROLE = (By.ID, "systemUser_userType")
    EMPLOYEE_NAME = (By.ID, "systemUser_employeeName_empName")
    NEW_USERNAME = (By.ID, "systemUser_userName")
    NEW_PASSWORD = (By.ID, "systemUser_password")
    CONFIRM_PASSWORD = (By.ID, "systemUser_confirmPassword")
    SAVE_BTN = (By.ID, "btnSave")
    SEARCH_USERNAME = (By.ID, "searchSystemUser_userName")
    SEARCH_BTN = (By.ID, "searchBtn")
    RESULT_TABLE = (By.ID, "resultTable")

    def go_to_users(self):
        self.click(self.USER_MANAGEMENT)
        self.click(self.USERS)

    def add_user(self, employee_name, username, password, role_index=1):
        self.click(self.ADD_BTN)
        # select role by index (simple approach)
        role_select = self.find(self.USER_ROLE)
        role_select.click()
        # fill fields
        self.send_keys(self.EMPLOYEE_NAME, employee_name)
        self.send_keys(self.NEW_USERNAME, username)
        self.send_keys(self.NEW_PASSWORD, password)
        self.send_keys(self.CONFIRM_PASSWORD, password)
        self.click(self.SAVE_BTN)

    def search_user(self, username):
        self.send_keys(self.SEARCH_USERNAME, username)
        self.click(self.SEARCH_BTN)
        table = self.find(self.RESULT_TABLE)
        return username in table.text
