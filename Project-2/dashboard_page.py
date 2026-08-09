from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    WELCOME = (By.ID, "welcome")
    MENU_ADMIN = (By.ID, "menu_admin_viewAdminModule")
    MENU_PIM = (By.ID, "menu_pim_viewPimModule")
    MENU_LEAVE = (By.ID, "menu_leave_viewLeaveModule")
    MENU_TIME = (By.ID, "menu_time_viewTimeModule")
    MENU_RECRUIT = (By.ID, "menu_recruitment_viewRecruitmentModule")
    MENU_MYINFO = (By.ID, "menu_pim_viewMyDetails")
    MENU_PERFORMANCE = (By.ID, "menu__Performance")
    MENU_DASHBOARD = (By.ID, "menu_dashboard_index")

    def is_logged_in(self):
        return self.is_visible(self.WELCOME)

    def logout(self):
        self.click(self.WELCOME)
        logout_locator = ("xpath", "//a[text()='Logout']")
        self.click((By.XPATH, "//a[text()='Logout']"))
