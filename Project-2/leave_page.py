from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LeavePage(BasePage):
    ASSIGN_LEAVE = (By.ID, "menu_leave_assignLeave")
    EMPLOYEE_NAME = (By.ID, "assignleave_txtEmployee_empName")
    LEAVE_TYPE = (By.ID, "assignleave_txtLeaveType")
    FROM_DATE = (By.ID, "assignleave_txtFromDate")
    TO_DATE = (By.ID, "assignleave_txtToDate")
    ASSIGN_BTN = (By.ID, "assignBtn")
    SUCCESS_MSG = (By.XPATH, "//div[contains(@class,'message success')]")

    def go_to_assign(self):
        self.click(self.ASSIGN_LEAVE)

    def assign_leave(self, employee, leave_type, from_date, to_date):
        self.send_keys(self.EMPLOYEE_NAME, employee)
        self.send_keys(self.FROM_DATE, from_date)
        self.send_keys(self.TO_DATE, to_date)
        # leave type selection simplified: send keys
        self.send_keys(self.LEAVE_TYPE, leave_type)
        self.click(self.ASSIGN_BTN)

    def get_success(self):
        el = self.is_visible(self.SUCCESS_MSG)
        return el.text if el else ""
