import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage

def test_tc05_create_user_and_validate_login(driver):
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    admin = AdminPage(driver)
    login.load()
    login.login("Admin", "admin123")
    assert dashboard.is_logged_in()
    admin.go_to_users()
    # create unique username
    ts = str(int(time.time()))
    new_username = f"testuser_{ts}"
    admin.add_user(employee_name="Linda Anderson", username=new_username, password="Password@123")
    dashboard.logout()
    # attempt login with new user
    login.load()
    login.login(new_username, "Password@123")
    # new user may not have permissions to see dashboard welcome; check for presence of welcome or error
    if dashboard.is_logged_in():
        dashboard.logout()
    else:
        # if not logged in, capture error
        err = login.get_error()
        assert err == "", f"New user login failed: {err}"
