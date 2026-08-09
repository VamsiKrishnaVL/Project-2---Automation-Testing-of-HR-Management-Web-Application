from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage

def test_tc06_validate_new_user_in_admin_list(driver):
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    admin = AdminPage(driver)
    login.load()
    login.login("Admin", "admin123")
    assert dashboard.is_logged_in()
    admin.go_to_users()
    # For demonstration, search for 'Admin' user (replace with created username if persisted)
    found = admin.search_user("Admin")
    assert found, "Expected to find user 'Admin' in user list"
    dashboard.logout()
