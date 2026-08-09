from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.leave_page import LeavePage

def test_tc09_assign_leave(driver):
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    leave = LeavePage(driver)
    login.load()
    login.login("Admin", "admin123")
    assert dashboard.is_logged_in()
    leave.go_to_assign()
    leave.assign_leave(employee="Linda Anderson", leave_type="Annual Leave", from_date="2026-08-10", to_date="2026-08-11")
    success = leave.get_success()
    assert success != "", "Expected success message after assigning leave"
    dashboard.logout()
